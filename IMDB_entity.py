import json
import logging

class IMDBEntity:

    order = None
    rating = None
    num_of_ratings = None
    num_of_oscars = None
    title = None


    def __init__(self, order, data):
        self.order = order

        # here should come a function which parses the data and creates a dict from JSON
        self.data = self.data_to_dict(data)

        # after the data is structured by the previous function, its data should be assigned to class variables
        self.model_data()

    def data_to_dict(self, data):
        return json.loads("".join(data))

    def model_data(self):
        self.parse_rating()
        self.parse_num_of_ratings()
        self.parse_num_of_oscars()

    def parse_rating(self):
        try:
            self.rating = self.data['props']['pageProps']['aboveTheFoldData']['ratingsSummary']['aggregateRating']
        except TypeError:
            logging.warning("Could not extract rating from movie data, value is set to 0!")
            self.rating = 0

    def parse_num_of_ratings(self):
        try:
            self.num_of_ratings = self.data['props']['pageProps']['aboveTheFoldData']['ratingsSummary']['voteCount']
        except TypeError:
            logging.warning("Could not extract num_of_ratings from movie data, value is set to 0!")
            self.num_of_ratings = 0

    def parse_num_of_oscars(self):
        try:
            self.num_of_oscars = self.data['props']['pageProps']['mainColumnData']['prestigiousAwardSummary']['wins']
        except TypeError:
            logging.warning("Could not extract num_of_oscars from movie data, value is set to 0!")
            self.num_of_oscars = 0

    def parse_title(self):
        try:
            self.title = self.data['props']['pageProps']['aboveTheFoldData']['titleText']['text']
        except TypeError:
            logging.warning("Could not extract title from movie data, value is set to ""!")
            self.title = ""

