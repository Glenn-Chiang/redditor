import os
from moviepy.editor import AudioFileClip, VideoFileClip, concatenate_audioclips


def combine_audio(input_dir: str, output_path: str):
    # Combine audio files in audio_dir. Sequence is determined by creation time of audio file.
    audio_files = [os.path.join(input_dir, file) for file in os.listdir(input_dir)]
    audio_files.sort(key=os.path.getctime)
    audio_clips = [AudioFileClip(file) for file in audio_files]
    combined_audio: AudioFileClip = concatenate_audioclips(audio_clips)
    combined_audio.write_audiofile(output_path)

if __name__ == '__main__':
    combine_audio(input_dir='tmp/audio', output_path='tmp/audio.wav')
