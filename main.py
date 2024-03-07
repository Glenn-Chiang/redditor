import os
from reddit_scraper import get_subreddit_thread
from text_to_speech import generate_audio
from screenshot import screenshot_post_and_comments

audio_directory = 'output/audio'

def main():
    target_subreddit = 'AskReddit'
    num_posts_required = 5
    comments_per_post = 5

    # Getting subreddit thread
    print(f'Getting thread from r/{target_subreddit}...')
    posts = get_subreddit_thread(subreddit_name=target_subreddit,
                                 num_posts_required=num_posts_required, comments_per_post=comments_per_post)

    # Generate audio files for each post/comment
    print('Generating audio...')
    for post in posts:
        # Generate audio for post title
        generate_audio(text=post['title'], output_path=os.path.join(audio_directory, f"t3_{post['id']}.wav"))
        # Generate audio for comments
        for comment in post['comments']:
            generate_audio(text=comment['body'], output_path=os.path.join(audio_directory, f"t1_{comment['id']}.wav"))

    # Get screenshot of each post/comment
    for post in posts:
        post_id = f"t3_{post['id']}"
        comment_ids = [f"t1_{comment['id']}" for comment in post['comments']]
        screenshot_post_and_comments(subreddit=target_subreddit, post_id=post_id, comment_ids=comment_ids, output_dir='output/screenshots')

    print('Done!')


if __name__ == '__main__':
    main()
