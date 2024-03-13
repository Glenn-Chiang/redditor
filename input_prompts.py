# Display list of items and prompt the user to select 1 item by its index number.
# Repeat the prompt until user enters valid input
def select_post(posts: list[dict]) -> dict:
    while True:
        print(f'Select post from below:')
        for index, post in enumerate(posts):
            print(f"[{index}] {post['url']}")
        
        user_input = input('Index number: ')

        try:
            selected_index = int(user_input)
            return posts[selected_index]
            
        except (ValueError, IndexError):
            print('Invalid index number\n')


def select_subreddit(subreddits: list[str]) -> str:
    while True:
        print(f'Select subreddit from below:')
        for index, subreddit in enumerate(subreddits):
            print(f"[{index}] {subreddit}")
        
        user_input = input('Index number: ')

        try:
            selected_index = int(user_input)
            return subreddits[selected_index]
            
        except (ValueError, IndexError):
            print('Invalid index number\n')