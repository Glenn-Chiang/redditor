import os
from reddit_scraper import get_subreddit_thread
from text_to_speech import generate_audio

audio_directory = 'output/audio'

def main():
    target_subreddit = 'AskReddit'
    num_posts_required = 1
    comments_per_post = 1

    # Getting subreddit thread...
    posts = get_subreddit_thread(subreddit_name=target_subreddit,
                                 num_posts_required=num_posts_required, comments_per_post=comments_per_post)

    for post in posts:
        # Generate audio for post title
        generate_audio(text=post['title'], output_path=os.path.join(audio_directory, f"{post['id']}.mp3"))
        # Generate audio for comments
        for comment in post['comments']:
            generate_audio(text=comment['body'], output_path=os.path.join(audio_directory, f"{post['id']}_{comment['id']}.mp3"))


if __name__ == '__main__':
    main()
