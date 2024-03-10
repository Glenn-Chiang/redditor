import os
import googleapiclient.discovery
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.http import MediaFileUpload

SCOPES = ['https://www.googleapis.com/auth/youtube.upload']

TOKEN_FILE = os.path.join(os.path.dirname(__file__), './token.json')
CLIENT_SECRETS_FILE = os.path.join(os.path.dirname(__file__), './client_secret.json')

VIDEO_DIRECTORY = 'output'


# Only need to run this function the first time you authenticate with google to obtain a refresh token
# The token will be saved and used to authenticate all subsequent requests
def get_token():
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, scopes=SCOPES)
    # Authenticate via browser
    credentials = flow.run_local_server()
    # Save token for future runs
    with open(TOKEN_FILE, 'w') as file:
        file.write(credentials.to_json())


def get_youtube_service():
    # Get new token if there is not saved token
    if not os.path.exists(TOKEN_FILE):
        get_token()
    credentials = Credentials.from_authorized_user_file(TOKEN_FILE, scopes=SCOPES)
    # Refresh token
    credentials.refresh(Request())

    return googleapiclient.discovery.build(serviceName='youtube', version='v3', credentials=credentials)


def upload_video(video_path, title, description):
    youtube = get_youtube_service()
    video_metadata = {
        'snippet': {
            'title': title,
            'description': description,
            'categoryId': 23
        }
    }

    request = youtube.videos().insert(body=video_metadata, media_body=MediaFileUpload(filename=video_path), part='contentDetails,snippet')
    response = request.execute()
    return response


def main():
    video_filenames = os.listdir(VIDEO_DIRECTORY)

    while True:
        print('Videos:')
        for index, filename in enumerate(video_filenames):
            print(f'[{index}] {filename}')
        user_input = input('Enter the index number of the video to upload: ')

        try:
            selected_option = int(user_input)
            selected_filename = video_filenames[selected_option]
            break
        except (ValueError, IndexError):
            print('Invalid index number')

    title_limit = 50
    while True:
        title = input('Enter a title for your video: ')
        if len(title) > title_limit:
            print(f'Title cannot be more than {title_limit} characters')
        else:
            break
    
    title = title or 'reddit compilation' # default title
    description = 'This video was generated by a python script. Source code at https://github.com/Glenn-Chiang/redditor.git.'

    video_path = os.path.join(VIDEO_DIRECTORY, selected_filename)
    response = upload_video(video_path=video_path, title=title, description=description)
    print(response)


if __name__ == '__main__':
    main()

