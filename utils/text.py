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
