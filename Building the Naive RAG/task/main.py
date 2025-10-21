from config import SCRIPTS_BASE_URL, MOVIES_BASE_URL
from ingestion import load_documents, chunk_document
from data import scrap_movies_data
from utils import clean_text
from ingestion.embedder import embed_and_store_scenes
from generation import rewrite_query
from retrieval import retrieve_scenes


def main():
    # 1. Collect movie title
    movies = scrap_movies_data(MOVIES_BASE_URL)

    # 2. Accept user search for movie
    movie_title = input(">")

    # 3. verify input
    if movie_title == "" or movie_title not in movies.values():
        print(f"Script for {movie_title} wasn't found in the list of movie scripts.")
        exit(0)

    # 4. Construct full script URL
    path = movie_title.strip().replace(" ", "-") + ".html"
    script_url = f"{SCRIPTS_BASE_URL}{path}"

    # 5. Load the movie's Script using LangChain - IMSDbLoader
    movie_script = load_documents(script_url)

    # 6. Clear script text
    cleaned_movie_script = clean_text(movie_script)

    # 7. Chunk script document
    chunked_script = chunk_document(cleaned_movie_script, 500, 10)

    # 8. Print the loaded movie + full url + script
    print("Loaded script for", movie_title, "from", script_url + ".")
    print()

    # 9. Display the number of split chunks
    print(f"Found {len(chunked_script)} scenes in the script for {movie_title}.")

    # 10. Use the embeddings model to generate vector representations scene chunks
    qdrant_vs = embed_and_store_scenes(chunked_script, movie_title)

    # 11. Get user query
    print()
    query = input(">").lower()

    # 12. Re-write user query
    rewritten_query = rewrite_query(query)

    # 13. Print the re-written query
    print(f'Rewritten query to: "{rewritten_query}."')
    print()

    # 14. Search query
    results = retrieve_scenes(rewritten_query, qdrant_vs)

    # 15. Print results
    for index, result in enumerate(results, start=1):
        print(f"Scene {index}: {result.page_content}")


if __name__ == "__main__":
    main()
