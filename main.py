import os
import shutil
from reddit_client import reddit_client
from text_to_speech import generate_audio
from screenshot_downloader import screenshot_post, screenshot_comment, screenshot_thread
from video_maker import make_video
from input_prompts import select_post, select_subreddit

output_directory = 'output'
temp_directory = 'tmp'
audio_directory = os.path.join(temp_directory, 'audio')
screenshot_directory = os.path.join(temp_directory, 'screenshots')
background_video_path = 'assets/background.mp4'

VIDEO_SIZE = (1080, 1920)  # width, height
MAX_DURATION = 45  # in seconds

subreddits = ['AskReddit', 'Showerthoughts', 'funny', 'AskMen']
# How many posts to fetch from the selected subreddit. User will be prompted to select a post from this list.
num_posts = 10
max_comments = 10


def generate():
    # Create necessary directories if they have not been created
    for dir_path in [audio_directory, screenshot_directory, output_directory]:
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

    target_subreddit = select_subreddit(subreddits)

    # Get trending posts from subreddit
    print(f'Getting posts from r/{target_subreddit}...')
    try:
        posts = reddit_client.get_posts(
            subreddit_name=target_subreddit, num_posts=num_posts)
    except Exception as error:
        print('Error getting posts:', error)
        return

    post = select_post(posts)

    print(f"\nSelected post {post['id']}: {post['title']} {'(nsfw)' if post['nsfw'] else ''}")
    print(f"Getting comments...")

    try:
        comments = reddit_client.get_comments(
            subreddit_name=target_subreddit, post_id=post['id'], num_comments=max_comments)
        post['comments'] = comments
    except Exception as error:
        print('Error getting comments:', error)
        return

    for comment in comments:
        print(f"https://www.reddit.com{comment['permalink']}")

    # Generate audio files for each post/comment
    print('\nGenerating audio...')

    # Generate audio for post title
    title_audio_filename = f"t3_{post['id']}.wav"
    try:
        generate_audio(text=post['title'], output_path=os.path.join(
            audio_directory, title_audio_filename))
        print('Generated audio:', title_audio_filename)
    except Exception as error:
        # If there was an error generating audio for post title, exit program
        print('Error generating audio for post:', error)
        return

    # Generate audio for comments
    for comment in comments:
        comment_audio_filename = f"t1_{comment['id']}.wav"
        try:
            generate_audio(text=comment['body'], output_path=os.path.join(
                audio_directory, comment_audio_filename))
            print('Generated audio:', comment_audio_filename)
        except Exception as error:
            # If there was an error generating audio for this comment, skip to next comment
            print(
                f"Error generating audio for comment {comment['id']}:", error)
            continue

    # TODO: Remove audio files of comments that would exceed video duration. Then, only download screenshots for remaining comments.

    print('\nDownloading screenshots...')

    screenshot_thread(subreddit=target_subreddit, post_id=f"t3_{post['id']}", comment_ids=[
                      f"t1_{comment['id']}" for comment in comments], output_dir=screenshot_directory, nsfw=post['nsfw'])

    print('Creating video...')
    video_filename = post['url'].split('/')[7] + '.mp4'
    output_path = os.path.join(output_directory, video_filename)
    make_video(audio_dir=audio_directory, image_dir=screenshot_directory, background_video_path=background_video_path,
               output_path=output_path, video_size=VIDEO_SIZE, max_duration=MAX_DURATION)

    print('Video generated!')

    # Remove temp directory
    shutil.rmtree(temp_directory)


if __name__ == '__main__':
    generate()
