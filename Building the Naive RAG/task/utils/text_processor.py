import re


def clean_text(script_text):
    # Replace sequence of white characters with s single space
    movie_script_cleaned = re.sub(r'\s+', ' ', script_text).strip()
    return movie_script_cleaned
