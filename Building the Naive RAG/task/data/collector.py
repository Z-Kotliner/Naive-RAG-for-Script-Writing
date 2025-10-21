import requests
from bs4 import BeautifulSoup

movies = {}


def scrap_movies_data(base_url) -> dict[int, str]:
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
    except requests.exceptions.RequestException as e:
        print(f"Error retrieving data from imsdb.com. {e}")

    return movies
