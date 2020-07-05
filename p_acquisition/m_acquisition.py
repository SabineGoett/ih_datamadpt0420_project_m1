import lxml
import re
from bs4 import BeautifulSoup
import pandas as pd
import requests
from sqlalchemy import create_engine
import numpy as np
import json
# acquisition functions


def raw_data_project_country_info (path):


    engine = create_engine(f'sqlite:///./{path}')

    df_country_info = pd.read_sql_query("SELECT * from country_info", engine)

    return df_country_info

def raw_data_project_career_info (path):


    engine = create_engine(f'sqlite:///{path}')

    df_career_info = pd.read_sql_query("SELECT * from career_info", engine)

    return df_career_info

def dic_country_codes ():
    url = 'ec.europa.eu/eurostat/statistics-explained/index.php/Glossary:Country_codes'
    html = requests.get(f'https://{url}').content
    soup = BeautifulSoup(html, 'lxml')
    list_int = [element.text for element in soup.find_all('table')]
    string = ''.join(list_int)
    country_list = string.split('\n')
    list_country = []
    list_keys = []
    list_empty = []
    for i in country_list:
        if '(' in i and i != 'China (except Hong Kong)':
            list_keys.append(i)
        elif i == '':
            list_empty.append(i)
        else:
            list_country.append(i)
    country_dictionary = dict(zip(list_keys, list_country))
    country_dictionary['GB'] = 'Great Britain'
    country_dictionary['GR'] = 'Greece'
    with open('country_dictionary.txt', 'w') as outfile:
        return json.dump(country_dictionary, outfile)

dic_country_codes ()

def get_country_dictionary():
    with open('country_dictionary.txt') as json_file:
        country_dictionary = json.load(json_file)
        return country_dictionary

def list_with_job_ids(job_code, columnname):
    list_ids = []
    l = job_code[columname].values.tolist()
    for x in l:
        if x != None:
            list_ids.append(x)
        s = set(list_ids)
        list_ids_unique = list(s)
    return list_ids_unique