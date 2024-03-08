import base64
import requests
from requests.exceptions import RequestException
from utils.text import split_text

# ENDPOINTS = ["https://tiktoktts.com/api/tiktok-tts"]
TEXT_CHAR_LIMIT = 299

def get_tts_response(text: str) -> str:
    try:
        res = requests.post(url='https://tiktok-tts.weilnet.workers.dev/api/generation',
                            json={'text': text, 'voice': 'en_us_001'})
        res.raise_for_status()
    except RequestException as error:
        raise RequestException(f'Error getting response from Tiktok text-to-speech API: {error}')
    return res.json()['data']


def generate_audio(text: str, output_path: str):
    if len(text) <= TEXT_CHAR_LIMIT:
        audio_encoding = get_tts_response(text)
    else:
        # If text exceeds limit accepted by API, split text into smaller chuinks then combine the output
        text_chunks = split_text(text, chunk_size=TEXT_CHAR_LIMIT)
        audio_encoding = ''.join([get_tts_response(text) for text in text_chunks])

    # Decode base64 string to binary
    audio_bytes = base64.b64decode(audio_encoding)

    with open(output_path, 'wb') as file:
        file.write(audio_bytes)


if __name__=='__main__':
    text = 'hello world'

    generate_audio(text=text, output_path='tmp/audio/test.wav')