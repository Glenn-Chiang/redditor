import re
import nltk
from nltk.tokenize import sent_tokenize

nltk.download('punkt')

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
