import os
from reddit_scraper import get_subreddit_thread
from text_to_speech import generate_audio
from screenshot_downloader import screenshot_post_and_comments
from requests.exceptions import RequestException

audio_directory = 'tmp/audio'
screenshot_directory = 'tmp/screenshots'

def main():
    target_subreddit = 'AskReddit'
    num_posts_required = 5
    comments_per_post = 5

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
            generate_audio(text=post['title'], output_path=os.path.join(audio_directory, filename))
            print('Generated audio:', filename)
        except Exception as error:
            # If there was an error generating audio for this post, skip to next post
            print(f"Error generating audio for post {post['id']}:", error)
            continue

        # Generate audio for comments
        for comment in post['comments']:
            filename = f"t1_{comment['id']}.wav"
            try:
                generate_audio(text=comment['body'], output_path=os.path.join(audio_directory, filename))
                print('Generated audio:', filename)
            except Exception as error:
                # If there was an error generating audio for this comment, skip to next comment
                print(f"Error generating audio for comment {comment['id']}:", error)
                continue

    # Get screenshot of each post/comment
    print('Downloading screenshots...')
    for post in posts:
        post_id = f"t3_{post['id']}"
        comment_ids = [f"t1_{comment['id']}" for comment in post['comments']]
        
        # screenshot_post_and_comments(subreddit=target_subreddit, post_id=post_id, comment_ids=comment_ids, output_dir=screenshot_directory)

    print('Done!')


if __name__ == '__main__':
    main()
