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
    countries = soup.text
    countries_Be_SE = countries [2184:2596]
    countries_UK = countries [2611:2639]
    countries_Iceland = countries [2683:2763]
    countries_Montenegro = countries[2791:2886]
    countries_Bosnia = countries[2949:3005]
    countries_Armenia = countries[3062:3174]
    countries_Algeria = countries[3233:3336]
    countries_Russia = countries[3465:3479]
    countries_Argentina = countries[3506:3819]
    countries_total = countries_Be_SE + countries_UK + countries_Iceland + countries_Montenegro + countries_Bosnia + countries_Armenia +countries_Algeria + countries_Russia + countries_Argentina
    countries_split_list = re.split('\n', countries_total)
    list_country = []
    list_keys = []
    list_empty = []
    for i in countries_split_list:
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