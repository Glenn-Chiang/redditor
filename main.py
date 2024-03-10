import os
import shutil
from uuid import uuid4
from reddit_scraper import get_subreddit_thread
from text_to_speech import generate_audio
from screenshot_downloader import screenshot_post_and_comments
from video_maker import make_video

output_directory = 'output'
temp_directory = 'tmp'
audio_directory = os.path.join(temp_directory, 'audio')
screenshot_directory = os.path.join(temp_directory, 'screenshots')
background_video_path = 'assets/gameplay.mp4'
video_size = (1080, 1920)
target_subreddit = 'AskReddit'
num_posts_required = 1
comments_per_post = 5


def main():
    # Create necessary directories if they have not been created
    for dir_path in [audio_directory, screenshot_directory, output_directory]:
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

    # Getting subreddit thread
    print(f'Getting thread from r/{target_subreddit}...')
    posts = get_subreddit_thread(subreddit_name=target_subreddit,
                                 num_posts_required=num_posts_required, comments_per_post=comments_per_post)

    for post in posts:
        print('Post:', post['url'])
        print('Comments:')
        for comment in post['comments']:
            print(f"https://www.reddit.com{comment['permalink']}")
        print('')

    # Generate audio files for each post/comment
    print('Generating audio...')
    for post in posts:
        # Generate audio for post title
        filename = f"t3_{post['id']}.wav"
        try:
            generate_audio(text=post['title'], output_path=os.path.join(
                audio_directory, filename))
            print('Generated audio:', filename)
        except Exception as error:
            # If there was an error generating audio for this post, skip to next post
            print(f"Error generating audio for post {post['id']}:", error)
            continue

        # Generate audio for comments
        for comment in post['comments']:
            filename = f"t1_{comment['id']}.wav"
            try:
                generate_audio(text=comment['body'], output_path=os.path.join(
                    audio_directory, filename))
                print('Generated audio:', filename)
            except Exception as error:
                # If there was an error generating audio for this comment, skip to next comment
                print(
                    f"Error generating audio for comment {comment['id']}:", error)
                continue

    # Get screenshot of each post/comment
    print('Downloading screenshots...')
    for post in posts:
        post_id = f"t3_{post['id']}"
        comment_ids = [f"t1_{comment['id']}" for comment in post['comments']]
        screenshot_post_and_comments(subreddit=target_subreddit, post_id=post_id,
                                     comment_ids=comment_ids, output_dir=screenshot_directory)

    print('Creating video...')
    output_path = os.path.join(output_directory, f'{uuid4()}.mp4')
    make_video(audio_dir=audio_directory, image_dir=screenshot_directory,
               background_video_path=background_video_path, output_path=output_path, video_size=video_size)

    print('Video created!')

    # Remove temp directory TODO: Uncomment this in production
    shutil.rmtree(temp_directory)


if __name__ == '__main__':
    main()
