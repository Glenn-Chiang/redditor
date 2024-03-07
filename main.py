from reddit_scraper import get_subreddit_thread


def main():
    target_subreddit = 'AskReddit'
    num_posts_required = 1
    comments_per_post = 1

    # Getting subreddit thread...
    posts = get_subreddit_thread(subreddit_name=target_subreddit,
                                 num_posts_required=num_posts_required, comments_per_post=comments_per_post)

    for post in posts:
        print(post)


if __name__ == '__main__':
    main()
