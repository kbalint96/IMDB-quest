from IMDB_scraper import IMDBScraper
from adjuster import Adjuster
import utils

utils.init_logging()

scraper = IMDBScraper("https://www.imdb.com/chart/top")
scraped_data = scraper.get_data()

imdb_entities = utils.build_imdb_entities(scraped_data)

adjuster = Adjuster(imdb_entities)
adjuster.adjust()

utils.data_to_json(imdb_entities)
utils.data_to_csv(imdb_entities)

