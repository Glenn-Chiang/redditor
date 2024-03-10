# redditor
A script that generates short-form videos from popular reddit threads

[![thumbnail](http://img.youtube.com/vi/goTNMh0OINo/0.jpg)](https://www.youtube.com/shorts/goTNMh0OINo)
[![thumbnail](http://img.youtube.com/vi/bDfnwqNr50g/0.jpg)](https://www.youtube.com/shorts/bDfnwqNr50g)

## How it works
1. Prompt user to select a subreddit to provide content for the video
2. Fetch trending posts from the selected subreddit using the reddit API
3. Prompt user to select one of the trending posts
4. Fetch top comments under the selected post using the reddit API
5. Generate voice-over audio for the post and its comments using the tiktok text-to-speech API
6. Download screenshots of the post and its comments using [playwright](https://github.com/microsoft/playwright-python)
7. Combine the screenshots and audio files together with a background clip to form a video using [moviepy](https://github.com/Zulko/moviepy/)

## Getting started
### Obtaining Reddit API credentials
1. Go to https://reddit.com/prefs/apps and follow the steps to register for usage of the Reddit API
2. Obtain a reddit client ID and client secret

### Installation and setup
1. Clone the repository and navigate to its directory
```
git clone https://github.com/Glenn-Chiang/redditor.git
cd redditor
```
2. Create a virtual environment and install dependencies
```
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
3. Create a `.env` file and fill in the values for `REDDIT_CLIENT_ID` and `REDDIT_CLIENT_SECRET` with the credentials you obtained from [Obtaining Reddit API credentials](#obtaining-reddit-api-credentials)
```
REDDIT_CLIENT_ID='your-client-id'
REDDIT_CLIENT_SECRET='your-client-secret'
```

### Usage
Run the script
```
python main.py
```
Warning: do not run the script on multiple terminal windows at the same time as doing so may cause the script to read the wrong files
