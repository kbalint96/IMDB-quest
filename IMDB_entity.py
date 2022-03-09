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
        """
        Constructor of IMDBEntity

        The class stores the data of a movie. Can be built from any IMDB movie JSON
        Constructor receives an ID and JSON, and start building up the data

        :param id: ID (or the original order) of the movie
        :param data: JSON data of the movie
        """
        self.id = id
        self.model_data(data)

    def data_to_dict(self, data):
        """
        Function to convert JSON to dictionary to be able to handle data

        :param data: JSON data of the movie
        :return: Movie data as dictionary
        """
        return json.loads("".join(data))

    def model_data(self, data):
        """
        Function to build up the entity, assign the corresponding values to class variables

        Data is being passed to all functions. In this way, it's not necessary to store the whole movie data in the entity,
        only the information we need.

        :param data: Movie data as dictionary
        :return: Nothing, but set the class variables through parsing methods
        """
        data = self.data_to_dict(data)
        self.parse_rating(data)
        self.parse_num_of_ratings(data)
        self.parse_num_of_oscars(data)
        self.parse_title(data)

    def parse_rating(self, data):
        """
        Function to parse rating information from movie data

        Sets default value if could not be found

        :param data: Movie data as dictionary
        :return: Sets the rating value of entity
        """
        try:
            self.rating = self.adjusted_rating = data['props']['pageProps']['aboveTheFoldData']['ratingsSummary']['aggregateRating']
        except TypeError:
            logging.warning("Could not extract rating from movie #%d data, value is set to %s!", self.id, utils.DEFAULT_DATA_VALUE_INT)
            self.rating = self.adjusted_rating = utils.DEFAULT_DATA_VALUE_INT


    def parse_num_of_ratings(self, data):
        """
        Function to parse number of rating information from movie data

        Sets default value if could not be found

        :param data: Movie data as dictionary
        :return: Sets the number of rating value of entity
        """
        try:
            self.num_of_ratings = data['props']['pageProps']['aboveTheFoldData']['ratingsSummary']['voteCount']
        except TypeError:
            logging.warning("Could not extract num_of_ratings from movie #%d data, value is set to %s!", self.id, utils.DEFAULT_DATA_VALUE_INT)
            self.num_of_ratings = utils.DEFAULT_DATA_VALUE_INT

    def parse_num_of_oscars(self, data):
        """
        Function to parse number of oscars information from movie data

        Sets default value if could not be found

        :param data: Movie data as dictionary
        :return: Sets the number of oscars value of entity
        """
        try:
            self.num_of_oscars = data['props']['pageProps']['mainColumnData']['prestigiousAwardSummary']['wins']
        except TypeError:
            logging.warning("Could not extract num_of_oscars from movie #%d data, value is set to %s!", self.id, utils.DEFAULT_DATA_VALUE_INT)
            self.num_of_oscars = utils.DEFAULT_DATA_VALUE_INT

    def parse_title(self, data):
        """
        Function to parse title information from movie data

        Sets default value if could not be found
        Using the encoding defined in utils to handle special characters

        :param data: Movie data as dictionary
        :return: Sets the title value of entity
        """
        try:
            self.title = data['props']['pageProps']['aboveTheFoldData']['titleText']['text']
            self.title.encode('utf8')
        except TypeError:
            logging.warning("Could not extract title from movie #%d data, value is set to %s!", self.id, utils.DEFAULT_DATA_VALUE_STR)
            self.title = utils.DEFAULT_DATA_VALUE_STR

    def adjust_rating(self, adjustment):
        """
        Function to manipulate rating information of the entity

        :param adjustment: Number to be added to the current adjusted_rating
        :return: Adds the param to adjusted_rating
        """
        self.adjusted_rating = round(self.adjusted_rating + adjustment, 2)

    def __str__(self):
        """
        Override str function to be able to print an entity better, in format of
        id, rating, adjusted_rating, num_of_ratings, num_of_oscars, title

        :return:
        """
        return "{}\t{}\t{}\t{}\t{}\t{}".format(self.id, self.rating, self.adjusted_rating, self.num_of_ratings, self.num_of_oscars, self.title)
