import os
from moviepy.editor import AudioFileClip, VideoFileClip, ImageClip, concatenate_videoclips


def make_video(audio_dir: str, image_dir: str, output_path: str):
    image_paths = [os.path.join(image_dir, file)
                   for file in os.listdir(image_dir)]
    # Sort image files by date created
    image_paths.sort(key=os.path.getctime)

    image_clips = []

    for image_path in image_paths:
        filename = os.path.splitext(os.path.basename(image_path))[0]
        # Get corresponding audio file from audio_dir. It is assumed to have the same filename as the image file.
        audio_path = os.path.join(audio_dir, filename + '.wav')

        # If there is no corresponding audio file for this image, skip the image
        if not os.path.exists(audio_path):
            continue

        audio_clip = AudioFileClip(filename=audio_path)
        image_clip: ImageClip = ImageClip(
            img=image_path, duration=audio_clip.duration).set_audio(audio_clip)
        # image_clip.write_videofile(output_path, fps=24)
        image_clips.append(image_clip)

    video = concatenate_videoclips(image_clips, method='compose')
    video.write_videofile(output_path, fps=1)


if __name__ == '__main__':
    make_video(audio_dir='tmp/audio', image_dir='tmp/screenshots',
               output_path='tmp/video/test.mp4')
