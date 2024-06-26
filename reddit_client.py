import requests
from requests.exceptions import RequestException
from requests.auth import HTTPBasicAuth
import os
from dotenv import load_dotenv
load_dotenv()

REDDIT_CLIENT_ID = os.getenv('REDDIT_CLIENT_ID')
REDDIT_CLIENT_SECRET = os.getenv('REDDIT_CLIENT_SECRET')
API_URL = 'https://oauth.reddit.com'

class RedditClient():
    session: requests.Session

    def __init__(self, client_id, client_secret) -> None:
        self.session = requests.Session()
        self.authenticate(client_id=client_id, client_secret=client_secret)

    # Request for auth token and attach it to request headers
    def authenticate(self, client_id: str, client_secret: str) -> None:
        basic_auth = HTTPBasicAuth(username=client_id, password=client_secret)
        payload = {'grant_type': 'client_credentials'}

        try:
            response = requests.post(
                'https://www.reddit.com/api/v1/access_token', auth=basic_auth, data=payload, headers={'User-Agent': 'reddit-scraper:1.0'})
            response.raise_for_status()
        except RequestException as error:
            raise RequestException(
                f'Error authenticating with reddit API: {error}')

        token = response.json()['access_token']

        self.session.headers.update({
            'Authorization': f'bearer {token}',
            'User-Agent': 'reddit-scraper:1.0'
        })

    # Get given number of posts for given subreddit

    def get_posts(self, subreddit_name: str, num_posts: int) -> list[dict]:
        try:
            response = self.session.get(
                f'{API_URL}/r/{subreddit_name}/best.json', params={'limit': num_posts})
            response.raise_for_status()
        except RequestException as error:
            raise RequestException(
                f'Error getting posts from subreddit: {error}')

        print(response.content)

        posts = [
            {
                'id': post['data']['id'],
                'title': post['data']['title'],
                'url': post['data']['url'],
                'nsfw': post['data']['over_18']
            } for post in  response.json()['data']['children']
        ]
        return posts

    # Get given number of comments for given post in subreddit

    def get_comments(self, subreddit_name: str, post_id: str, num_comments: int) -> list[dict]:
        try:
            response = self.session.get(
                f'{API_URL}/r/{subreddit_name}/comments/{post_id}/best.json')
            response.raise_for_status()
        except RequestException as error:
            raise RequestException(
                f'Error getting comments for post: {error}')

        comments = response.json()[1]['data']['children'][:-1][:num_comments]

        return [{
            'id': comment['data']['id'],
            'body': comment['data']['body'],
            'permalink': comment['data']['permalink']
        } for comment in comments]


reddit_client = RedditClient(
    client_id=REDDIT_CLIENT_ID, client_secret=REDDIT_CLIENT_SECRET)
