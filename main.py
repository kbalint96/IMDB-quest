from IMDB_scraper import IMDBScraper
from IMDB_entity import IMDBEntity
import logging

"""
The IMDB quest can be used to scrape, parse, adjust and reorder data from IMDB which can be written into CSV.

@TODO: IMDB_scaper - A class which can be constructed with a URL and can transform an URL to raw data of the website.
@TODO: IMDB_entity - A class which holds the structure of an IMDB entity: title, rating, num_of_ratings, num_of_ocars
                     Also responsible to build the entity from given raw data
@TODO: calculator - A class which is responsible for data manipulation and adjustments
"""

logging.getLogger().setLevel(logging.INFO)

scraper = IMDBScraper("https://www.imdb.com/chart/top")
scraped_data = scraper.get_data()

imdb_entities = []
for i in range(len(scraped_data)):
    imdb_entities.append(IMDBEntity(i + 1, scraped_data[i]))


