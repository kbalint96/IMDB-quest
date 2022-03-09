# IMDB-quest
Scrape IMDB movies from any IMDB chart site, adjust them based on preferences and export in JSON or CSV

Main modules:
1) IMDB_scraper
2) IMDB_entity
3) adjuster
4) utils

## utils
The utils contains CONSTANTs and class-independent functions, such as logging, exporting and converting

## IMDBScraper
A class which is responsible for extract movie data as JSON from a given IMDB chart URL

The constructor of the class needs an IMDB chart URL. By calling the constructor and creating the object, all functions
will automatically be called.
```
scraper = IMDBScraper("https://www.imdb.com/chart/boxoffice")
```

To get data, the data getter should be called, which returns a list of JSON movie data
```
scraped_data = scraper.get_data()
```

## IMDBEntity
A class which stores movie data (order, original rating, adjusted rating, number of ratings, number or oscars and title as an object
The build_imdb_entities function of utils returns a list of IMDBEntity object converted from the scraped_data
```
imdb_entities = utils.build_imdb_entities(scraped_data)
```

## Adjuster
Since we live in a perfectly fair world, the original ratings should be adjusted based on number of oscars and number of ratings.
More or less, the more oscar a movie has, the most extra point it gets, meanwhile the less number of rating it has, the more penalty it gets.

The adjuster can be called right on the imdb_entity list, which adjust all elements separately and resort the list based on the new ratings.
```
adjuster = Adjuster(imdb_entities)
adjuster.adjust()
```

## Exporting
All the lists with IMDBEntity objects (either original or adjusted) can be exported as JSON or CSV files.
The name and path of the output files can be configured in utils.
```
utils.data_to_json(imdb_entities)
utils.data_to_csv(imdb_entities)
```

##Main
By the end, the main should look like
```
from IMDB_scraper import IMDBScraper
from adjuster import Adjuster
import utils

utils.init_logging()

scraper = IMDBScraper("https://www.imdb.com/chart/boxoffice")
scraped_data = scraper.get_data()

imdb_entities = utils.build_imdb_entities(scraped_data)

adjuster = Adjuster(imdb_entities)
adjuster.adjust()

utils.data_to_json(imdb_entities)
utils.data_to_csv(imdb_entities)
```