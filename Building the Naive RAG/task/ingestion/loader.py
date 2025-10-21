import os

os.environ[
    'USER_AGENT'] = "'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"

from langchain_community.document_loaders import IMSDbLoader


# Document Loader
def load_documents(movie_url):
    loader = IMSDbLoader(movie_url)
    data = loader.load()
    content = data[0].page_content
    return content
