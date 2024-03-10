import requests
from requests.exceptions import RequestException
from requests.auth import HTTPBasicAuth
import os
from dotenv import load_dotenv
load_dotenv()

REDDIT_CLIENT_ID = os.getenv('REDDIT_CLIENT_ID')
REDDIT_CLIENT_SECRET = os.getenv('REDDIT_CLIENT_SECRET')
API_URL = 'https://oauth.reddit.com'


# Request for auth token and attach it to request headers
def authenticate_session(session: requests.Session, client_id: str, client_secret: str) -> requests.Session:
    basic_auth = HTTPBasicAuth(username=client_id, password=client_secret)
    payload = {'grant_type': 'client_credentials'}

    try:
        response = requests.post(
            'https://www.reddit.com/api/v1/access_token', auth=basic_auth, data=payload, headers={'User-Agent': 'reddit-scraper:1.0'})
        response.raise_for_status()
    except RequestException:
        raise

    token = response.json()['access_token']

    session.headers.update({
        'Authorization': f'bearer {token}',
        'User-Agent': 'reddit-scraper:1.0'
    })

    return session


# Get given number of posts for given subreddit
def get_posts(session: requests.Session, subreddit_name: str, num_posts: int) -> list[dict]:
    try:
        response = session.get(
            f'{API_URL}/r/{subreddit_name}/top', params={'limit': num_posts})
        response.raise_for_status()
    except RequestException as error:
        raise RequestException(f'Error getting posts from subreddit: {error}')

    response_data = response.json()['data']
    posts = [
        {
            'id': post['data']['id'],
            'title': post['data']['title'],
            'url': post['data']['url'],
        } for post in response_data['children']
    ]
    return posts


# Get given number of comments for given post in subreddit
def get_comments(session: requests.Session, subreddit_name: str, post_id: str, num_comments: int):
    comments = []
    last_comment_id = None

    # You're probably wondering why we can't just make a single batch request for the required number of comments.
    # The truth is, I have no idea. The API just always decides to return fewer comments than what was requested.
    while len(comments) < num_comments:
        try:
            response = session.get(
                f'{API_URL}/r/{subreddit_name}/comments/{post_id}', params={'after': last_comment_id})
            response.raise_for_status()
        except RequestException as error:
            raise RequestException(f'Error getting comments for post: {error}')

        last_comment_id = response.json()[1]['data']['after']

        for comment in response.json()[1]['data']['children'][:-1]:
            if len(comments) < num_comments:
                comments.append({
                    'id': comment['data']['id'],
                    'body': comment['data']['body'],
                    'permalink': comment['data']['permalink']
                })
            else:
                break

    return comments


# Get given number of posts for given subreddit, with given number of comments nested under each post object
def get_subreddit_thread(subreddit_name: str, num_posts_required: int, comments_per_post: int) -> list[dict]:
    session = requests.Session()
    try:
        session = authenticate_session(
            session=session, client_id=REDDIT_CLIENT_ID, client_secret=REDDIT_CLIENT_SECRET)
    except RequestException as error:
        raise RequestException(
            f'Error authenticating with reddit API: {error}')

    posts = get_posts(
        session=session, subreddit_name=subreddit_name, num_posts=num_posts_required)

    # Add corresponding comments to each post object
    for post in posts:
        comments = get_comments(
            session=session, subreddit_name=subreddit_name, post_id=post['id'], num_comments=comments_per_post)
        post['comments'] = comments

    return posts


if __name__ == '__main__':
    target_subreddit = 'AskReddit'
    num_posts_required = 1
    # How many comments to read for each post
    comments_per_post = 10
    posts = get_subreddit_thread(subreddit_name=target_subreddit,
                                 num_posts_required=num_posts_required, comments_per_post=comments_per_post)
    for post in posts:
        comments = post['comments']
        for comment in comments:
            print(comment['body'])
