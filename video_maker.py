import random
import os
from moviepy.editor import AudioFileClip, VideoFileClip, ImageClip, CompositeVideoClip, concatenate_videoclips
from moviepy.video.fx.crop import crop
import PIL.Image


# Extract, crop and resize a random clip from a video to use as background clip
def get_background_clip(video_path: str, duration: int, size: tuple[int, int]) -> VideoFileClip:
    source_video = VideoFileClip(video_path)
    
    # If source video is longer than 
    if source_video.duration > duration:
        start_time = random.randint(
            0, int(source_video.duration) - duration)
        clip: VideoFileClip = source_video.subclip(
            start_time, start_time + duration)

    original_width, original_height = clip.size
    original_aspect_ratio = original_width / original_height

    target_width, target_height = size
    target_aspect_ratio = target_width / target_height

    cropped_width = original_width if original_aspect_ratio <= target_aspect_ratio else int(
        original_height * target_aspect_ratio)
    cropped_height = original_height if original_aspect_ratio > target_aspect_ratio else int(
        original_width / target_aspect_ratio)

    cropped_clip: VideoFileClip = crop(
        clip=clip, width=cropped_width, height=cropped_height, x_center=clip.size[0]//2, y_center=clip.size[1]//2)
    return cropped_clip.resize(size, PIL.Image.LANCZOS)


def make_video(audio_dir: str, image_dir: str, background_video_path: str, output_path: str, video_size: tuple[int, int]) -> None:
    image_paths = [os.path.join(image_dir, file)
                   for file in os.listdir(image_dir)]
    # Sort image files by date created
    image_paths.sort(key=os.path.getctime)

    background_video = VideoFileClip(background_video_path)

    # Combine each image with its corresponding audio
    image_clips = []
    total_duration = 0

    for image_path in image_paths:
        filename = os.path.splitext(os.path.basename(image_path))[0]
        # Get corresponding audio file from audio_dir. It is assumed to have the same filename as the image file.
        audio_path = os.path.join(audio_dir, filename + '.wav')

        # If there is no corresponding audio file for this image, skip the image
        if not os.path.exists(audio_path):
            continue

        audio_clip = AudioFileClip(filename=audio_path)

        # If adding the next clip would cause the duration to exceed that of the background video, stop adding clips
        if total_duration + audio_clip.duration > background_video.duration:
            break

        image_clip: ImageClip = ImageClip(img=image_path, duration=audio_clip.duration).set_audio(audio_clip)
        image_clips.append(image_clip)
        total_duration += image_clip.duration        

    # Video containing sequence of images
    images_video = concatenate_videoclips(image_clips, method='compose')
    # image_video.write_videofile(output_path, fps=1)
    print('Duration:', images_video.duration)

    background_video = get_background_clip(
        video_path=background_video_path, duration=int(images_video.duration), size=video_size)

    composite_video = CompositeVideoClip(
        [background_video, images_video.set_position('center')])
    composite_video.write_videofile(output_path)


if __name__ == '__main__':
    make_video(audio_dir='tmp/audio', image_dir='tmp/screenshots',
               background_video_path='assets/gameplay.mp4', output_path='tmp/video/test.mp4', video_size=(1080, 1920))
