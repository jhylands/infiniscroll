import requests
from bs4 import BeautifulSoup, NavigableString
# The purpose of this module is simply to get a feed
# So at the moment this is basically the requests get call


def get_feed(url):
    result = requests.get(url)
    if result.status_code != 200:
        raise Exception(result)
    return result.content


def parse(result):
    soup = BeautifulSoup(result, features='xml')
    articles = soup.findAll("item")
    if len(articles) == 0:
        articles = soup.findAll("entry")
        # Might also need record, statement, listing, article, element

    parsed_articles = []
    for article in articles:
        parsed_article = {}
        for child in article.children:
            if isinstance(child, NavigableString):
                continue
            parsed_article[child.name] = child.attrs
            if child.text != "":
                parsed_article[child.name]["innerHTML"] = child.text
        parsed_articles.append(parsed_article)

    return parsed_articles
