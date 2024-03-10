import base64
import requests
from requests.exceptions import RequestException
import re
import nltk
from nltk.tokenize import sent_tokenize

# Download tokenizer if it has not been downloaded
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

# ENDPOINTS = ["https://tiktoktts.com/api/tiktok-tts"]
TEXT_CHAR_LIMIT = 299


def split_text(text: str, chunk_size: int):
    # Replace newlines when periods
    sentences: list[str] = sent_tokenize(re.sub('\n+', '. ', text))

    # Split sentences into chunks
    # We are trying to avoid splitting a single sentence across multiple chunks.
    text_chunks = []
    current_chunk = ''
    for sentence in sentences:
        if (len(current_chunk) + len(sentence) <= chunk_size):
            # Add sentence to current chunk
            current_chunk += ' ' + sentence
            # If sentence doesn't end with a period and the chunk is still within chunk_size, add a period.
            if not sentence.endswith('.') and len(current_chunk) < chunk_size:
                current_chunk += '.'
        else:
            # If adding the next sentence would exceed chunk_size, stop adding to current chunk and begin a new chunk.
            if current_chunk:
                text_chunks.append(current_chunk.strip())
            current_chunk = ''

            # If sentence fits chunk_size, add the whole sentence to the next chunk
            if len(sentence) <= chunk_size:
                current_chunk = sentence
            # If sentence exceeds chunk_size, we have no choice but to split the sentence into multiple chunks
            else:
                for word in sentence.split():
                    if len(current_chunk) + len(word) <= chunk_size:
                        current_chunk += ' ' + word
                    else:
                        if current_chunk:
                            text_chunks.append(current_chunk.strip())
                        current_chunk = word

    if current_chunk:
        text_chunks.append(current_chunk.strip())
    return text_chunks


def get_tts_response(text: str) -> str:
    try:
        res = requests.post(url='https://tiktok-tts.weilnet.workers.dev/api/generation',
                            json={'text': text, 'voice': 'en_us_001'})
        res.raise_for_status()
    except RequestException as error:
        raise RequestException(
            f'Error getting response from Tiktok text-to-speech API: {error}')
    return res.json()['data']


def generate_audio(text: str, output_path: str):
    if len(text) <= TEXT_CHAR_LIMIT:
        audio_encoding = get_tts_response(text)
    else:
        # If text exceeds limit accepted by API, split text into smaller chuinks then combine the output
        text_chunks = split_text(text, chunk_size=TEXT_CHAR_LIMIT)
        audio_encoding = ''.join([get_tts_response(text)
                                 for text in text_chunks])

    # Decode base64 string to binary
    audio_bytes = base64.b64decode(audio_encoding)

    with open(output_path, 'wb') as file:
        file.write(audio_bytes)


if __name__ == '__main__':
    text = 'hello world'

    generate_audio(text=text, output_path='tmp/audio/test.wav')
