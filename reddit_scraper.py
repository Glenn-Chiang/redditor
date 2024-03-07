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


def get_posts(session: requests.Session, subreddit_name: str, limit: int, after: str = None) -> list[dict]:
    try:
        response = session.get(
            f'{API_URL}/r/{subreddit_name}/top', params={'limit': limit, 'after': after})
        response.raise_for_status()
    except RequestException as error:
        raise RequestException(f'Error getting posts from subreddit: {error}')

    response_data = response.json()['data']
    posts = [
        {
            'id': post['data']['id'],
            'title': post['data']['title'],
            'url': post['data']['url']
        } for post in response_data['children']
    ]
    return posts


def get_comments(session: requests.Session, subreddit_name: str, post_id: str, comment_count: int):
    try:
        response = session.get(
            f'{API_URL}/r/{subreddit_name}/comments/{post_id}', params={'limit': comment_count})
        response.raise_for_status()
    except RequestException as error:
        raise RequestException(f'Error getting comments for post: {error}')

    comments = [
        {
            'body': comment['data']['body'],
            'permalink': comment['data']['permalink']
        } for comment in response.json()[1]['data']['children'][:-1]
    ]
                
    return comments


def get_subreddit_thread(subreddit_name: str, num_posts_required: int, comments_per_post: int):
    session = requests.Session()
    try:
        session = authenticate_session(
            session=session, client_id=REDDIT_CLIENT_ID, client_secret=REDDIT_CLIENT_SECRET)
    except RequestException as error:
        raise RequestException(
            f'Error authenticating with reddit API: {error}')

    posts = get_posts(
        session=session, subreddit_name=subreddit_name, limit=num_posts_required)

    for post in posts:
        post_title = post['title']
        post_url = post['url']
        post_id = post['id']
        print(post_id)
        print(post_title)
        print(post_url)

        comments = get_comments(
            session=session, subreddit_name=subreddit_name, post_id=post_id, comment_count=comments_per_post)
        for comment in comments:
            print(comment['body'])
            print(comment['permalink'])

        print('')


if __name__ == '__main__':
    target_subreddit = 'AskReddit'
    num_posts_required = 1
    # How many comments to read for each post
    comments_per_post = 1
    get_subreddit_thread(subreddit_name=target_subreddit,
                         num_posts_required=num_posts_required, comments_per_post=comments_per_post)
