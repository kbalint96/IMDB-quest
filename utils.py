import requests as r

IMDB_TITLE_COLUMN = "td.titleColumn a"
IMDB_SOUP_PARSER = "html.parser"
IMDB_TOP_RESULTS = 1

def transform_url(url):
    return r.get(url).text

