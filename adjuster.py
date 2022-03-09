import logging

class Adjuster:

    def __init__(self, imdb_entities):
        """
        Class which is responsible for adjustments logics
        Can be initialized with a list of IMDBEntity objects

        :param imdb_entities: IMDBEntity objects to be adjusted
        """
        self.imdb_entities = imdb_entities

    def get_max_num_of_ratings(self):
        """
        Function to determine the maximum number of ratings of given objects

        :return: the maximum num_of_ratings integer value
        """
        return max(entity.num_of_ratings for entity in self.imdb_entities)

    def adjust(self):
        """
        Function to apply all adjustments on each element of the entity list

        Adjusts ratings by oscar_calculator return value
        Adjusts ratings by review_penalizer return value
        Sorts the list based on the new ratings
        """

        logging.info("Adjusting movie ratings ...")

        for imdb_entity in self.imdb_entities:
            imdb_entity.adjust_rating(self.oscar_calculator(imdb_entity.num_of_oscars))
            imdb_entity.adjust_rating(self.review_penalizer(imdb_entity.num_of_ratings))

        self.sort_by_adjusted_rating()

        logging.info("Movie ratings successfully adjusted!")


    def sort_by_adjusted_rating(self):
        """
        Function to sort the list of IMDBEntity objects based on adjusted_rating
        """
        self.imdb_entities.sort(key=lambda x: x.adjusted_rating, reverse = True)

    def oscar_calculator(self, oscars):
        """
        Function to calculate the bonus points for ratings based on num_of_oscars

        :param imdb_entity: IMDBEntity objects to be analyzed
        :return: adjustment as float
        """

        if 1 <= oscars <= 2:
            return 0.3
        elif 3 <= oscars <= 5:
            return 0.5
        elif 6 <= oscars <= 10:
            return 1
        elif 10 < oscars:
            return 1.5
        else:
            return 0

    def review_penalizer(self, num_of_ratings):
        """
        Function to calculate the bonus points for ratings based on number of ratings

        :param imdb_entity: IMDBEntity objects to be analyzed
        :return: adjustment as float
        """
        max_num_of_ratings = self.get_max_num_of_ratings()
        return (max_num_of_ratings - num_of_ratings) // 100000 * (-0.1)