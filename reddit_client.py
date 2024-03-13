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
            raise RequestException(f'Error authenticating with reddit API: {error}')

        token = response.json()['access_token']

        self.session.headers.update({
            'Authorization': f'bearer {token}',
            'User-Agent': 'reddit-scraper:1.0'
        })


    # Get given number of posts for given subreddit
    def get_posts(self, subreddit_name: str, num_posts: int) -> list[dict]:
        try:
            response = self.session.get(
                f'{API_URL}/r/{subreddit_name}/best', params={'limit': num_posts})
            response.raise_for_status()
        except RequestException as error:
            raise RequestException(
                f'Error getting posts from subreddit: {error}')

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
    def get_comments(self, subreddit_name: str, post_id: str, num_comments: int) -> list[dict]:
        comments = []
        last_comment_id = None

        # You're probably wondering why we can't just make a single batch request for the required number of comments.
        # One would think that the 'limit' parameter would strictly determine the number of comments returned, but for some reason the API usually returns fewer comments than the requested limit, which is why we have to resort to this while loop.
        while len(comments) < num_comments:
            try:
                response = self.session.get(
                    f'{API_URL}/r/{subreddit_name}/comments/{post_id}/best', params={'limit': num_comments, 'after': last_comment_id})
                response.raise_for_status()
            except RequestException as error:
                raise RequestException(
                    f'Error getting comments for post: {error}')

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


reddit_client = RedditClient(client_id=REDDIT_CLIENT_ID, client_secret=REDDIT_CLIENT_SECRET)
