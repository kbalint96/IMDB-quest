class Adjuster:

    def __init__(self, imdb_entities):
        self.imdb_entities = imdb_entities
        self.max_num_of_ratings = self.set_max()

    def set_max(self):
        return max(entity.num_of_ratings for entity in self.imdb_entities)

    def adjust(self):
        for imdb_entity in self.imdb_entities:
            imdb_entity.adjustRating(self.oscar_calculator(imdb_entity))
            imdb_entity.adjustRating(self.review_penalizer(imdb_entity))

        self.sort_by_rating()

    def sort_by_rating(self):
        self.imdb_entities.sort(key=lambda x: x.rating, reverse = True)

    def oscar_calculator(self, imdb_entity):
        oscars = imdb_entity.num_of_oscars

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

    def review_penalizer(self, imdb_entity):
        return (self.max_num_of_ratings - imdb_entity.num_of_ratings) // 100000 * (-0.1)