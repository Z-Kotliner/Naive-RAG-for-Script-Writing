import os

os.environ[
    'USER_AGENT'] = "'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"

from langchain_text_splitters import RecursiveCharacterTextSplitter


# Chunker for script splitting
def chunk_document(doc, size: int, overlap: int):
    text_splitter = RecursiveCharacterTextSplitter(separators=["INT."], chunk_size=size, chunk_overlap=overlap)
    return text_splitter.split_text(doc)
