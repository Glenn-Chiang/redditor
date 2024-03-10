# redditor
A script that generates short-form videos from popular reddit threads

## How it works

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
4. Create an `assets` directory and add a `.mp4` video file named `background.mp4` to be used as the background clip for the video.

### Usage
Run the script
```
python main.py
```
