import os
import shutil
from uuid import uuid4
from reddit_client import reddit_client
from text_to_speech import generate_audio
from screenshot_downloader import screenshot_post, screenshot_comment
from video_maker import make_video

output_directory = 'output'
temp_directory = 'tmp'
audio_directory = os.path.join(temp_directory, 'audio')
screenshot_directory = os.path.join(temp_directory, 'screenshots')
background_video_path = 'assets/gameplay.mp4'

video_size = (1080, 1920)  # width, height
max_video_duration = 60  # in seconds

target_subreddit = 'AskReddit'
num_posts = 10 # How many posts to fetch from subreddit. User will be prompted to select a post from this list to use as the subject of the video.
comments_per_post = 5 # How many comments to include per video


def generate():
    # Create necessary directories if they have not been created
    for dir_path in [audio_directory, screenshot_directory, output_directory]:
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

    # Get trending posts from subreddit
    print(f'Getting posts from r/{target_subreddit}...')
    try:
        posts = reddit_client.get_posts(subreddit_name=target_subreddit, num_posts=num_posts)
    except Exception as error:
        print('Error getting posts:', error)
        return

    # Display list of trending posts and prompt user to select 1 post
    # Repeat the prompt until user enters valid input
    while True:
        print(f'Select a post from below:')
        for index, post in enumerate(posts):
            print(f"[{index}] {post['url']}")
        
        user_input = input('Index number: ')

        try:
            selected_index = int(user_input)
            post = posts[selected_index]
            break
        except (ValueError, IndexError):
            print('Invalid index number\n')
    
    print(f"\nSelected post {post['id']}")
    print(f"Getting comments...")
    
    try:
        comments = reddit_client.get_comments(subreddit_name=target_subreddit, post_id=post['id'], num_comments=comments_per_post)
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
        print(f'Error generating audio for post title')
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
            print(f"Error generating audio for comment {comment['id']}:", error)
            continue

    # Download screenshot of each post/comment
    print('\nDownloading screenshots...')
    post_id = f"t3_{post['id']}"
    try:
        screenshot_post(subreddit=target_subreddit, post_id=post_id,
                    output_path=os.path.join(screenshot_directory, f'{post_id}.png'))
        print('Downloaded screenshot:', post_id)
    except Exception as error:
        print(f"Error downloading screenshot for post {post_id}:", error)
        return

    for comment in comments:
        comment_id = f"t1_{comment['id']}"
        try:
            screenshot_comment(subreddit=target_subreddit, post_id=post_id, comment_id=comment_id,
                            output_path=os.path.join(screenshot_directory, f'{comment_id}.png'))
            print('Downloaded screenshot:', comment_id)
        except Exception as error:
            print(f"Error downloading screenshot for comment {comment_id}:", error)
            continue
            
    print('Creating video...')
    output_path = os.path.join(output_directory, f"{post['id']}.mp4")
    make_video(audio_dir=audio_directory, image_dir=screenshot_directory, background_video_path=background_video_path,
               output_path=output_path, video_size=video_size, max_duration=max_video_duration)

    print('Video generated!')

    # Remove temp directory TODO: Uncomment this in production
    shutil.rmtree(temp_directory)


if __name__ == '__main__':
    generate()
