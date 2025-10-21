from langchain_huggingface import HuggingFaceEndpointEmbeddings
import os
from qdrant_client.models import VectorParams, Distance
from langchain_core.documents import Document
from langchain_qdrant import QdrantVectorStore, Qdrant
from qdrant_client import QdrantClient
import dotenv

# Load API keys as environment variables
dotenv.load_dotenv()


# A function to initialize HF embeddings
def get_embeddings_model():
    embeddings_model = HuggingFaceEndpointEmbeddings(
        model="sentence-transformers/all-MiniLM-L6-v2",
        huggingfacehub_api_token=os.getenv("HF_API_KEY"),
    )
    return embeddings_model


def embed_and_store_scenes(scene_list, movie_title):
    # Connect to local Qdrant db
    client = QdrantClient("http://127.0.0.1:6333")

    # Construct Qdrant collection name
    collection_name = movie_title.strip().replace(" ", "-")

    # Create a langchain document objects
    script_langchain_docs = [Document(page_content=scene_chunk) for scene_chunk in scene_list]

    # Create collection in Qdrant if it does not exist
    if not client.collection_exists(collection_name):
        client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(size=384, distance=Distance.COSINE),
        )

    # Init embedding model
    embeddings_model = get_embeddings_model()

    # Init Qdrant vector store langchain wrapper
    qdrant_vs = QdrantVectorStore(
        embedding=embeddings_model,
        collection_name=collection_name,
        client=client
    )

    # Add documents to vector store
    qdrant_vs.add_documents(script_langchain_docs)

    # Inform user
    print(f"Embedded script for {movie_title}.")
