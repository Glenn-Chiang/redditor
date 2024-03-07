import requests
from requests.exceptions import RequestException
from requests.auth import HTTPBasicAuth
import os
from dotenv import load_dotenv
load_dotenv()

REDDIT_CLIENT_ID = os.getenv('REDDIT_CLIENT_ID')
REDDIT_CLIENT_SECRET = os.getenv('REDDIT_CLIENT_SECRET')


# Request for auth token and attach it to request headers
def authenticate_session(session: requests.Session, client_id: str, client_secret: str) -> requests.Session:
    basic_auth = HTTPBasicAuth(username=client_id, password=client_secret)
    payload = {'grant_type': 'client_credentials'}

    try:
        response = requests.post(
            'https://www.reddit.com/api/v1/access_token', auth=basic_auth, data=payload)
        response.raise_for_status()
    except RequestException:
        raise

    token = response.json()['access_token']

    session.headers.update({
        'Authorization': f'bearer {token}',
        'User-Agent': 'reddit-scraper:1.0'
    })

    return session


def get_subreddit_posts(subreddit_name: str, limit: int, after: str = None) -> tuple[list, str]:
    session = requests.Session()

    try:
        session = authenticate_session(
            session=session, client_id=REDDIT_CLIENT_ID, client_secret=REDDIT_CLIENT_SECRET)
    except RequestException as error:
        raise RequestException(
            f'Error authenticating with reddit API: {error}')

    try:
        response = session.get(
            f'https://oauth.reddit.com/r/{subreddit_name}/top', params={'limit': limit, 'after': after})
        response.raise_for_status()
    except RequestException as error:
        raise RequestException(f'Error getting posts from subreddit: {error}')

    response_data = response.json()['data']
    posts = [post['data'] for post in response_data['children']]
    last_post_id: str = response_data['after']
    return posts, last_post_id


if __name__ == '__main__':
    posts, last_post_id = get_subreddit_posts(subreddit_name='AskReddit', limit=1)
    for post in posts:
        print(post['title'])
        print(post['selftext_html'])
        print(post['url'])
        print(post['num_comments'])