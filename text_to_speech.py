import base64
import requests
from requests.exceptions import RequestException
import re


def split_text(text: str, chunk_size: int):
    sentences = re.split(r'([.!?])', text)
    text_chunks = []
    current_chunk = ""
    for sentence in sentences:
        if (len(current_chunk) + len(sentence) <= chunk_size):
            # Add to current chunk
            current_chunk += ' ' + sentence
        else:
            # Add current chunk to all chunks and start a new chunk
            if current_chunk:
                text_chunks.append(current_chunk.strip())
            current_chunk = sentence
    if current_chunk:
        text_chunks.append(current_chunk.strip())
    return text_chunks


def generate_audio(text: str) -> str:
    try:
        res = requests.post(url='https://tiktok-tts.weilnet.workers.dev/api/generation',
                            json={'text': text, 'voice': 'en_us_001'})
        res.raise_for_status()
    except RequestException as error:
        raise RequestException(f'Error getting response from Tiktok text-to-speech API: {error}')
    return res.json()['data']


def text_to_speech(text: str, output_path: str):
    TEXT_CHAR_LIMIT = 299
    if len(text) <= TEXT_CHAR_LIMIT:
        audio_encoding = generate_audio(text)
    else:
        # If text exceeds limit accepted by API, split text into smaller chuinks then combine the output
        text_chunks = split_text(text, chunk_size=TEXT_CHAR_LIMIT)
        audio_encoding = ''.join([generate_audio(text) for text in text_chunks])

    # Decode base64 string to binary
    audio_bytes = base64.b64decode(audio_encoding)

    with open(output_path, 'wb') as file:
        file.write(audio_bytes)


if __name__=='__main__':
    generate_audio(text='hello world. testing tiktok text to speech.', output_path='output/audio/test.wav')