from bs4 import BeautifulSoup
import utils
import logging
import requests

class IMDBScraper:

    movie_data = []
    movie_urls = []

    def __init__(self, url):
        """
        Constructor of IMDBScraper. Sets the chart URL and starts processing it

        :param url: the chart URL to be scraped
        """
        self.movie_urls = self.gen_urls_from_chart_site(url)
        self.movie_data = self.gen_movie_data()


    def get_data(self):
        """
        Data getter
        :return: self.movie_data
        """
        return self.movie_data

    def gen_urls_from_chart_site(self, url):
        """
        Function to collect movie URLs from an IMDB chart site

        Exits with 10 if chart link could not be parsed

        :param url: URL of the chart site,  i.e. https://www.imdb.com/chart/top/ or https://www.imdb.com/chart/boxoffice
        :return: list of movie URLs         i.e. ["https://www.imdb.com/title/tt0111161", ...]
        """

        logging.info("Scraping URLs from %s ...", url)

        movie_urls = []
        top_titles = []

        try:
            soup = BeautifulSoup(utils.transform_url(url), utils.IMDB_SOUP_PARSER)
            top_titles = soup.select(utils.IMDB_TITLE_COLUMN)
        except Exception:
            logging.error("Could not parse URL %s", url)
            exit(10)

        results_to_extract = min(len(top_titles), utils.IMDB_TOP_RESULTS)
        if results_to_extract != utils.IMDB_TOP_RESULTS:
            logging.warning("Actual results are less then the desired top results! Will only extract %d movie data", results_to_extract)

        for i in range(results_to_extract):
            logging.info("Getting URL of movie #%s", i+1)
            movie_urls.append("https://www.imdb.com/" + top_titles[i].get('href'))

        return movie_urls

    def gen_movie_data(self):
        """
        Function to extract JSON data from all given movie URLs

        Skips an URL if JSON could not be extracted

        :return: list of JSONs with movie data
        """

        logging.info("Extracting information from movie URLs ...")

        movie_data = []

        for i in range(len(self.movie_urls)):
            logging.info("Getting DATA of movie %s", i + 1)
            try:
                movie_data.append(BeautifulSoup(requests.get(self.movie_urls[i]).content, utils.IMDB_SOUP_PARSER).find('script', {'type': 'application/json'}))
            except Exception:
                logging.error("ERROR while extracting JSON from movie: %s", self.movie_urls[i])

        return movie_data