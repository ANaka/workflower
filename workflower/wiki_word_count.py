import redun
from redun import task
from scipy import stats
import numpy as np
import requests
import json
from bs4 import BeautifulSoup

redun_namespace = "redun.examples.wiki_word_count"

def get_random_article_id()->str:
    """
    Get the ID of a random Wikipedia article

    Returns:
        int: ID of the randomly selected article
    """
    url = "https://en.wikipedia.org/w/api.php?action=query&list=random&rnnamespace=0&format=json"

    response = requests.get(url)

    if response.status_code == 200:
        data = json.loads(response.text)
        random_article_id = data["query"]["random"][0]["id"]
    return random_article_id

@task()
def get_article_extract(article_id):
    """
    Get the extract of a Wikipedia article

    Args:
        article_id (int): ID of the article

    Returns:
        str: Extract of the article
    """
    article_url = "https://en.wikipedia.org/w/api.php?action=query&prop=extracts&format=json&pageids=" + str(random_article_id)
    article_response = requests.get(article_url)
    if article_response.status_code == 200:
        article_data = json.loads(article_response.text)
        article_extract = article_data["query"]["pages"][str(article_id)]["extract"]
        return article_extract

@task()
def get_article_text(article_id):
    """
    Get the full text of a Wikipedia article

    Args:
        article_id (int): ID of the article

    Returns:
        str: Full text of the article
    """
    full_article_url = "https://en.wikipedia.org/wiki?curid=" + str(article_id)

    article_response = requests.get(full_article_url)
    if article_response.status_code == 200:
        article_html = article_response.text
        return article_html

@task()
def parse_article_html(article_html):
    """
    Parse the HTML content of a Wikipedia article

    Args:
        article_html (str): HTML content of the article

    Returns:
        str: Text content of the article
    """
    soup = BeautifulSoup(article_html, "html.parser")
    article_text = soup.find('div', {'class': 'mw-parser-output'}).get_text()
    return article_text

@task()
def count_words_in_article_text(article_text):
    """
    Count the number of words in an article's text

    Args:
        article_text (str): Text content of the article

    Returns:
        int: Number of words in the article text
    """
    return len(article_text.split())

@task()
def get_first_digit(n):
    """
    Get the first digit of a number

    Args:
        n (int): The number

    Returns:
        int: The first digit of the number
    """
    return int(str(n)[0])

@task()
def main(n_articles:int=100):   
    results = []
    for _ in range(n_articles):
        random_article_id = get_random_article_id()
        article_extract = get_article_extract(random_article_id)
        article_html = get_article_text(random_article_id)
        article_text = parse_article_html(article_html)
        n_words = count_words_in_article_text(article_text)
        first_digit = get_first_digit(n_words)
        result = {"article_id": random_article_id, "n_words": n_words, "first_digit": first_digit}
        results.append(result)
    return results