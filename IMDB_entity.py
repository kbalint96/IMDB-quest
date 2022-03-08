import json

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
        self.parse_title()

    def parse_rating(self):
        self.rating = self.data['props']['pageProps']['aboveTheFoldData']['ratingsSummary']['aggregateRating']

    def parse_num_of_ratings(self):
        self.num_of_ratings = self.data['props']['pageProps']['aboveTheFoldData']['ratingsSummary']['voteCount']

    def parse_num_of_oscars(self):
        self.num_of_oscars = self.data['props']['pageProps']['mainColumnData']['prestigiousAwardSummary']['wins']

    def parse_title(self):
        self.title = self.data['props']['pageProps']['aboveTheFoldData']['titleText']['text']

