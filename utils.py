import requests as r
from IMDB_entity import IMDBEntity
import json
import time

IMDB_TITLE_COLUMN = "td.titleColumn a"
IMDB_SOUP_PARSER = "html.parser"
IMDB_TOP_RESULTS = 10
DEFAULT_DATA_VALUE_INT = 0
DEFAULT_DATA_VALUE_STR = ""

def transform_url(url):
    return r.get(url).text

def list_to_nested_dictionary(entities_list):
    entities_dict = {}
    for i in range(len(entities_list)):
        entities_dict[i] = vars(entities_list[i])

    return entities_dict

def data_to_json(data):
    with open("imdb_quest" + str(time.time()) + ".json", "w", encoding='UTF-8') as json_file:
        json.dump(data, json_file)