from typing import List

from langchain_qdrant import QdrantVectorStore
from langchain_core.documents import Document


# Performs similarity search on the Qdrant vector store
def retrieve_scenes(query, qdrant_vs: QdrantVectorStore) -> List[Document]:
    # results = qdrant_vs.similarity_search(query, k=5)

    # Convert vector-store to a retriever & return 5 results
    retriever = qdrant_vs.as_retriever(search_kwargs={"k": 5})

    # Invoke retrieval - calls similarity_search under the hood
    results = retriever.invoke(query)

    return results
