from bs4 import BeautifulSoup
import utils
import logging
import requests

class IMDBScraper:

    movie_data = []
    movie_urls = []

    def __init__(self, url):
        self.movie_urls = self.gen_urls_from_chart_site(url)
        self.movie_data = self.gen_movie_data()


    def get_data(self):
        return self.movie_data

    def gen_urls_from_chart_site(self, url):

        logging.info("Scraping URLs from %s", url)

        soup = BeautifulSoup(utils.transform_url(url), utils.IMDB_SOUP_PARSER)
        top_titles = soup.select(utils.IMDB_TITLE_COLUMN)
        movie_urls = []

        for i in range(utils.IMDB_TOP_RESULTS):
            logging.info("Get URL of movie #%s", i+1)
            movie_urls.append("https://www.imdb.com/" + top_titles[i].get('href'))

        return movie_urls

    def gen_movie_data(self):

        movie_data = []

        for i in range(len(self.movie_urls)):
            logging.info("Get DATA of movie %s", i + 1)
            movie_data.append(BeautifulSoup(requests.get(self.movie_urls[i]).content, utils.IMDB_SOUP_PARSER).find('script', {'type': 'application/json'}))

        return movie_data