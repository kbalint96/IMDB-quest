import unittest
import utils
from IMDB_scraper import IMDBScraper
from IMDB_entity import IMDBEntity
from unittest.mock import patch, mock_open
from adjuster import Adjuster
import os


class TestUtils:

    utils.IMDB_TOP_RESULTS = 2
    scraper = IMDBScraper("https://www.imdb.com/chart/top")

""" SCRAPER TESTS """
class TestIMDBScraperFunctions(unittest.TestCase):

    def test_gen_urls_from_chart_site(self):
        actual = IMDBScraper.gen_urls_from_chart_site(TestUtils.scraper, "https://www.imdb.com/chart/top")
        self.assertTrue(len(actual) == 2)
        self.assertTrue("https" in actual[0] and "https" in actual[1])


    def test_gen_movie_data(self):
        actual = IMDBScraper.gen_movie_data(TestUtils.scraper)
        self.assertTrue(type(actual[0]).__name__ == 'Tag')
        self.assertTrue(len(actual) == 2)


    def test_get_data(self):
        actual = IMDBScraper.get_data(TestUtils.scraper)
        expected = IMDBScraper.gen_movie_data(TestUtils.scraper)
        self.assertTrue(len(actual) == len(expected))
        self.assertTrue(type(actual) == type(expected))


""" IMDB ENTITY TESTS """
class TestIMDBEntityFunctions(unittest.TestCase):

    def test_all(self):
        actual = IMDBEntity(1, TestUtils.scraper.get_data()[0])
        self.assertEqual(len(vars(actual)), 6)
        self.assertEqual(actual.id, 1)

    def test_adjust_rating(self):
        actual = IMDBEntity(1, TestUtils.scraper.get_data()[0])

        actual.adjust_rating(0.5)
        self.assertEqual(actual.adjusted_rating, actual.rating + 0.5)

        actual.adjust_rating(-1)
        self.assertEqual(actual.adjusted_rating, actual.rating - 0.5)


""" ADJUSTER TESTS """
class TestAdjusterFunctions(unittest.TestCase):

    def test_oscar_calculator(self):
        data = [IMDBEntity(1, TestUtils.scraper.get_data()[0])]
        adjuster = Adjuster(data)
        num_of_oscars = 5
        actual = adjuster.oscar_calculator(num_of_oscars)
        expected = 0.5
        self.assertEqual(actual, expected)

    def test_review_penalizer(self):
        data = [IMDBEntity(1, TestUtils.scraper.get_data()[0])]
        data[0].num_of_ratings = 9500001
        adjuster = Adjuster(data)

        num_of_ratings = 5000000

        actual = adjuster.review_penalizer(num_of_ratings)
        expected = (-4.5)

        self.assertEqual(actual, expected)


""" UTIL TESTS """
class TestUtilFunctions(unittest.TestCase):

    def test_transform_url(self):
        actual = utils.transform_url("https://www.imdb.com/chart/top")
        self.assertTrue("<!DOCTYPE html>" in actual)


    def test_build_imdb_entities(self):
        actual = utils.build_imdb_entities(TestUtils.scraper.get_data())
        for entity in actual:
            self.assertTrue(type(entity).__name__ == "IMDBEntity")

        self.assertTrue(len(actual) == len(TestUtils.scraper.get_data()))


    def test_data_to_json(self):
        data = utils.build_imdb_entities(TestUtils.scraper.get_data())
        filename = os.getcwd() + utils.OUTPUT_FOLDER + utils.OUTPUT_FILENAME + ".json"

        open_mock = mock_open()
        with patch("utils.open", open_mock, create=True):
            utils.data_to_json(data)

        open_mock.assert_called_with(filename, "w", encoding='utf-8')
        open_mock.return_value.write()


    def test_data_to_csv(self):
        data = utils.build_imdb_entities(TestUtils.scraper.get_data())
        filename = os.getcwd() + utils.OUTPUT_FOLDER + utils.OUTPUT_FILENAME + ".csv"

        open_mock = mock_open()
        with patch("utils.open", open_mock, create=True):
            utils.data_to_csv(data)

        open_mock.assert_called_with(filename, "w", newline='')
        open_mock.return_value.write()


    def test_list_to_nested_dictionary(self):
        data = utils.build_imdb_entities(TestUtils.scraper.get_data())
        actual = utils.list_to_nested_dictionary(data)

        self.assertTrue(len(data) == len(actual))

        for i in range(len(actual)):
            self.assertEqual(actual[i]['id'], data[i].id)
            self.assertTrue(len(actual[i]) == len(vars(data[i])))