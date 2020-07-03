import re
from bs4 import BeautifulSoup
import pandas as pd
import requests
from sqlalchemy import create_engine
import numpy as np

def get_json_data(list_path):
    list_json_results = []
    for x in list_path:
        response = requests.get(f'http://{x}')
        json_data = response.json()
        list_json_results.append(json_data)
    return list_json_results

def get_job_dictionary(job_name_uuid):
    id_list = [c['uuid'] for c in job_name_uuid]
    job_name_list = [c['title'] for c in job_name_uuid]
    job_dictionary = dict(zip(id_list, job_name_list))
    return job_dictionary

def change_to_job_name (raw_table, job_dictionary):
    series_job_id = raw_table['normalized_job_code']
    series_job_id = np.where(series_job_id.isnull(),'none', series_job_id)
    final_list_job_name = [job_dictionary[id] if id != 'none' else id for id in series_job_id]
    raw_table['normalized_job_code'] = pd.Series(final_list_job_name)
    return raw_table['normalized_job_code']

def clean_country_dicctionary(dic_country):
    list_dic_c = list(dic_country)
    new_list = []
    for k in list_dic_c:
        x = k
        if ('(') in x and (')') in x:
            u = x[x.find('('):x.find(')')]
            t = u[1:]
            new_list.append(t)
        else:
            t = x
            new_list.append(t)
    new_values= list(dic_country.values())
    country_clean_dictionary = dict(zip(new_list, new_values))
    return country_clean_dictionary

def change_to_country_name (raw_table, country_clean_dictionary):
    series_country_code = raw_table['country_code']
    final_list_country_name = [country_clean_dictionary[code] if code != ' ' else code for code in series_country_code]
    raw_table['country_code'] = pd.Series(final_list_country_name)
    return raw_table['country_code']

def clean_rural_column (raw_table):
    raw_table['rural'] = np.where(raw_table.rural.str.contains('Country') | raw_table.rural.str.contains('countryside'), 'rural', raw_table['rural'])
    raw_table['rural'] = np.where(raw_table.rural.str.contains('city') | raw_table.rural.str.contains('Non-Rural'), 'urban', raw_table['rural'])
    return raw_table['rural']

def add_quantity_column(raw_table):
    l = len(raw_table)
    raw_table['Quantity'] = np.ones(l)
    raw_table['Quantity'] = raw_table['Quantity'].astype(int)
    return raw_table['Quantity']

def group_raw_table(raw_table):
    raw_grouped_table = raw_table.groupby(['country_code', 'normalized_job_code', 'rural']).sum()
    grouped_table_1 = raw_grouped_table.stack().reset_index()
    grouped_table_2 = grouped_table_1[['country_code', 'normalized_job_code', 'rural', 0]]
    filter1 = grouped_table_2['normalized_job_code'] != 'none'
    grouped_table_3 = grouped_table_2[filter1]
    grouped_table = grouped_table_3.rename(columns = {'country_code':'Country', 'normalized_job_code': 'Jobs', 'rural':'Area', 0: 'Quantity'})
    return grouped_table

def add_percentage_column(grouped_table):
    grouped_table['Percentage'] = ((grouped_table['Quantity'] / len(grouped_table))*100).round(2)
    grouped_table['Percentage'] = grouped_table['Percentage'].astype(str)
    grouped_table['Percentage'] = grouped_table['Percentage'] + '%'
    return (grouped_table['Percentage'])

def country_input(raw_table, chosen_country):
    lll = raw_table['country_code'].unique()
    cc = list(lll)
    if chosen_country in cc:
        print('you have chosen the country', chosen_country)
        chosen_country_final = chosen_country
    else:
        chosen_country_final = 'all'
        print('this country does not exist in the table. I will print you the table with all countries.')
    return chosen_country_final



def choose_country(grouped_table, chosen_country_final):
    ll = grouped_table['Country'].unique()
    list_countries = list(ll)
    list_filtered_df = []
    for x in list_countries:
        country_filter = grouped_table['Country'] == x
        u = grouped_table[country_filter]
        list_filtered_df.append(u)
    t = len(list_countries)
    list_numeros = list(range(t))
    dic_countries_numeros = dict(zip(list_countries, list_numeros))
    if chosen_country_final == 'all':
        country_df = grouped_table
    else:
        country_input = chosen_country_final
        k = dic_countries_numeros[country_input]
        country_df = list_filtered_df[dic_countries_numeros[country_input]]
    return country_df

