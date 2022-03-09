import json
import logging
import utils

class IMDBEntity:

    id = None
    rating = None
    adjusted_rating = None
    num_of_ratings = None
    num_of_oscars = None
    title = None


    def __init__(self, id, data):
        self.id = id

        # after the data is structured by the previous function, its data should be assigned to class variables
        self.model_data(data)

    def data_to_dict(self, data):
        return json.loads("".join(data))

    def model_data(self, data):
        data = self.data_to_dict(data)
        self.parse_rating(data)
        self.parse_num_of_ratings(data)
        self.parse_num_of_oscars(data)
        self.parse_title(data)

    def parse_rating(self, data):
        try:
            self.rating = self.adjusted_rating = data['props']['pageProps']['aboveTheFoldData']['ratingsSummary']['aggregateRating']
        except TypeError:
            logging.warning("Could not extract rating from movie #%d data, value is set to %s!", self.id, utils.DEFAULT_DATA_VALUE_INT)
            self.rating = self.adjusted_rating = utils.DEFAULT_DATA_VALUE_INT


    def parse_num_of_ratings(self, data):
        try:
            self.num_of_ratings = data['props']['pageProps']['aboveTheFoldData']['ratingsSummary']['voteCount']
        except TypeError:
            logging.warning("Could not extract num_of_ratings from movie #%d data, value is set to %s!", self.id, utils.DEFAULT_DATA_VALUE_INT)
            self.num_of_ratings = utils.DEFAULT_DATA_VALUE_INT

    def parse_num_of_oscars(self, data):
        try:
            self.num_of_oscars = data['props']['pageProps']['mainColumnData']['prestigiousAwardSummary']['wins']
        except TypeError:
            logging.warning("Could not extract num_of_oscars from movie #%d data, value is set to %s!", self.id, utils.DEFAULT_DATA_VALUE_INT)
            self.num_of_oscars = utils.DEFAULT_DATA_VALUE_INT

    def parse_title(self, data):
        try:
            self.title = data['props']['pageProps']['aboveTheFoldData']['titleText']['text']
            self.title.encode('utf8')
        except TypeError:
            logging.warning("Could not extract title from movie #%d data, value is set to %s!", self.id, utils.DEFAULT_DATA_VALUE_STR)
            self.title = utils.DEFAULT_DATA_VALUE_STR

    def adjust_rating(self, adjustment):
        self.adjusted_rating = round(self.adjusted_rating + adjustment, 2)

    def __str__(self):
        return "{}\t{}\t{}\t{}\t{}\t{}".format(self.id, self.rating, self.adjusted_rating, self.num_of_ratings, self.num_of_oscars, self.title)
