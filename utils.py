import requests as r
import json
from datetime import datetime
import csv
import os
from IMDB_entity import IMDBEntity
import logging

"""
The utils is supposed to store CONSTANTS and functions which do not have strong dependency of other classes
"""

LOGGING_LEVEL = logging.INFO
IMDB_TOP_RESULTS = 20
FILE_ENCODING = "utf-8"
OUTPUT_FOLDER = "\\output\\"
OUTPUT_FILENAME = "IMDB_TOP-" + str(IMDB_TOP_RESULTS) + (datetime.now().strftime("%Y%m%dT%H%M%S"))
DEFAULT_DATA_VALUE_INT = 0
DEFAULT_DATA_VALUE_STR = ""
IMDB_TITLE_COLUMN = "td.titleColumn a"
IMDB_SOUP_PARSER = "html.parser"


def init_logging():
    """
    Function to set logging level based on util constant
    """
    logging.getLogger().setLevel(LOGGING_LEVEL)

def transform_url(url):
    """
    Function to extract text (HTML) from any URL
    :param url: URL as object
    :return: URL as str
    """
    return r.get(url).text

def build_imdb_entities(data):
    """
    Function to convert any list storing movie JSON data into list of IMDBEntity objects

    :param data: List of movie data as JSON
    :return: List of IMDBEntity objects
    """

    logging.info("Creating IMDBEntities out of movie JSON data ...")
    imdb_entities = []
    for i in range(len(data)):
        try:
            imdb_entities.append(IMDBEntity(i + 1, data[i]))
        except Exception as e:
            logging.error("IMDBEntity could not be created! Skipping data ...", e)

    return imdb_entities

def list_to_nested_dictionary(entities_list):
    """
    Function to create a nested dictionary from list of IMDBEntity objects to be able to handle JSONs better

    :param entities_list: List of IMDBEntity objects
    :return: Nested dictionary as
    {
        0: {dict_of_object_1},
        1: {dict_of_object_2},
        ...
    }
    """
    entities_dict = {}
    for i in range(len(entities_list)):
        entities_dict[i] = vars(entities_list[i])

    return entities_dict

def data_to_json(data):
    """
    Function to create JSON out of any dictionary and write into file

    :param data: Data as dictionary
    :return: Creates .json file
    """

    logging.info("Creating JSON file to %s...", os.getcwd() + OUTPUT_FOLDER)

    data = list_to_nested_dictionary(data)
    os.makedirs(os.getcwd() + OUTPUT_FOLDER, exist_ok=True)

    try:
        with open(os.getcwd() + OUTPUT_FOLDER + OUTPUT_FILENAME + ".json", "w", encoding=FILE_ENCODING) as json_file:
            json.dump(data, json_file, ensure_ascii=False)
        logging.info("JSON file successfully created as %s", os.getcwd() + OUTPUT_FOLDER + OUTPUT_FILENAME + ".json")
    except Exception as e:
        logging.error("JSON file could not be created!", e)


def data_to_csv(data):
    """
    Function to create a CSV file out of list of IMDBEntity objects

    :param data: Data as list of IMDBEntity objects
    :return: Creates .csv file
    """

    logging.info("Creating CSV file to %s...", os.getcwd() + OUTPUT_FOLDER)

    os.makedirs(os.getcwd() + OUTPUT_FOLDER, exist_ok=True)

    try:
        with open(os.getcwd() + OUTPUT_FOLDER + OUTPUT_FILENAME + ".csv", "w", newline='') as csv_file:
            wr = csv.writer(csv_file)
            wr.writerow(["Title", "Original order", "Original rating", "Adjusted rating", "Number of ratings", "Number of oscars"])
            for row in data:
                wr.writerow([row.title, row.id, row.rating, row.adjusted_rating, row.num_of_ratings, row.num_of_oscars])
            logging.info("CSV file successfully created as %s", os.getcwd() + OUTPUT_FOLDER + OUTPUT_FILENAME + ".csv")
    except Exception as e:
        logging.error("CSV file could not be created!", e)

