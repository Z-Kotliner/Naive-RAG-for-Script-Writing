import os

os.environ[
    'USER_AGENT'] = "'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"

import requests
from bs4 import BeautifulSoup
from langchain_community.document_loaders import IMSDbLoader

base_url = "https://imsdb.com/all-scripts.html"
scripts_base_url = "https://imsdb.com/scripts/"

movies = {}


def main():
    # Retrieve all movies from IMSDb
    try:
        response = requests.get(base_url)
        response.raise_for_status()
        # Parse it using BeautifulSoup & display movies list
        soup = BeautifulSoup(response.content, "html.parser")
        paragraphs = soup.find_all("p")
        for index, paragraph in enumerate(paragraphs):
            movie_link = paragraph.find("a")
            movies[index] = movie_link.text
            print(f"{index}. {movie_link.text}")
    except requests.exceptions.RequestException as e:
        print(f"Error retrieving data from imsdb.com. {e}")

        print()

    # Accept user search for movie
    movie_title = input()

    # verify input
    if movie_title == "" or movie_title not in movies.values():
        print(f"Script for {movie_title} wasn't found in the list of movie scripts.")
        exit(0)

    # Construct full script URL
    path = movie_title.strip().replace(" ", "-") + ".html"
    movie_url = f"{scripts_base_url}{path}"
    # print(f"Movie URL: {movie_url}")

    # Load the movie's Script using LangChain - IMSDbLoader
    loader = IMSDbLoader(movie_url)
    data = loader.load()
    content = data[0].page_content

    # Print the loaded movie + full url + script
    print("Loaded script for", movie_title, "from", movie_url + ".")

    # Print Script
    print(content)


if __name__ == "__main__":
    main()
