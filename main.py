import os
import shutil
from uuid import uuid4
from reddit_scraper import get_subreddit_thread
from text_to_speech import generate_audio
from screenshot_downloader import screenshot_post, screenshot_comment
from video_maker import make_video

output_directory = 'output'
temp_directory = 'tmp'
audio_directory = os.path.join(temp_directory, 'audio')
screenshot_directory = os.path.join(temp_directory, 'screenshots')
background_video_path = 'assets/gameplay.mp4'
video_size = (1080, 1920)  # width, height
max_video_duration = 40  # in seconds
target_subreddit = 'AskReddit'
num_posts_required = 1
comments_per_post = 30  # This will fetch all comments for the post


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
                print(f"Error generating audio for comment {comment['id']}:", error)
                continue

    # Download screenshot of each post/comment
    print('Downloading screenshots...')
    for post in posts:
        post_id = f"t3_{post['id']}"
        try:
            screenshot_post(subreddit=target_subreddit, post_id=post_id,
                        output_path=os.path.join(screenshot_directory, f'{post_id}.png'))
            print('Downloaded screenshot:', post_id)
        except Exception as error:
            print(f"Error downloading screenshot for post {post_id}:", error)
            continue

        for comment in post['comments']:
            comment_id = f"t1_{comment['id']}"
            try:
                screenshot_comment(subreddit=target_subreddit, post_id=post_id, comment_id=comment_id,
                               output_path=os.path.join(screenshot_directory, f'{comment_id}.png'))
                print('Downloaded screenshot:', comment_id)
            except Exception as error:
                print(f"Error downloading screenshot for comment {comment_id}:", error)
                continue
            
    print('Creating video...')
    output_path = os.path.join(output_directory, f'{uuid4()}.mp4')
    make_video(audio_dir=audio_directory, image_dir=screenshot_directory, background_video_path=background_video_path,
               output_path=output_path, video_size=video_size, max_duration=max_video_duration)

    print('Video created!')

    # Remove temp directory TODO: Uncomment this in production
    shutil.rmtree(temp_directory)


if __name__ == '__main__':
    main()
