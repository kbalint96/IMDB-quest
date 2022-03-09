import requests as r
import json
from datetime import datetime
import csv
import os

IMDB_TITLE_COLUMN = "td.titleColumn a"
IMDB_SOUP_PARSER = "html.parser"
IMDB_TOP_RESULTS = 3
DEFAULT_DATA_VALUE_INT = 0
DEFAULT_DATA_VALUE_STR = ""
FILE_ENCODING = "iso-8859-1"
OUTPUT_FOLDER = "/output/"

def transform_url(url):
    return r.get(url).text

def list_to_nested_dictionary(entities_list):
    entities_dict = {}
    for i in range(len(entities_list)):
        entities_dict[i] = vars(entities_list[i])

    return entities_dict

def data_to_json(data):
    os.makedirs(os.getcwd() + OUTPUT_FOLDER, exist_ok=True)
    with open(os.getcwd() + OUTPUT_FOLDER + "imdb_quest-" + (datetime.now().strftime("%Y%m%dT%H%M%S")) + ".json", "w", encoding=FILE_ENCODING) as json_file:
        json.dump(data, json_file, ensure_ascii=False)

def data_to_csv(data):
    os.makedirs(os.getcwd() + OUTPUT_FOLDER, exist_ok=True)
    with open(os.getcwd() + OUTPUT_FOLDER + "imdb_quest-" + (datetime.now().strftime("%Y%m%dT%H%M%S")) + ".csv", "w", newline='') as csv_file:
        wr = csv.writer(csv_file)
        wr.writerow(["Title", "Original order", "Original rating", "Adjusted rating", "Number of ratings", "Number of oscars"])
        for row in data:
            wr.writerow([row.title, row.id, row.rating, row.adjusted_rating, row.num_of_ratings, row.num_of_oscars])

