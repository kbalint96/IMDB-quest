class IMDBEntity:

    order = None
    rating = None
    num_of_rating = None
    num_of_oscars = None
    title = None

    def __init__(self, order, data):
        self.order = order
        self.data = data

        # here should come a function which parses the data and creates an array or dict from the movie
        self.data_to_dict()

        # after the data is structured by the previous function, its data should be assigned to class variables
        self.model_data()

    def data_to_dict(self):
        return

    def model_data(self):
        return

    def parse_rating(self):
        return

    def parse_num_of_ratings(self):
        return

    def parse_num_of_oscars(self):
        return

    def parse_title(self):
        return