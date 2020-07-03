import argparse
import pandas as pd
from sqlalchemy import create_engine
import re
from bs4 import BeautifulSoup
from p_acquisition import m_acquisition as mac
from p_analysis import m_analysis as man
from p_wrangling import m_wrangling as mwr
from p_reporting import m_reporting as mre

def argument_parser():
    parser = argparse.ArgumentParser(description='specify inputs')
    parser.add_argument('-p','--path', help='introduce...', type = str, required=True)
    parser.add_argument('-j','--job_path', help='get...', type = str, required=True)
    args = parser.parse_args()
    return args

def main(args):
    df_country_info = mac.raw_data_project_country_info(args.path)
    df_career_info = mac.raw_data_project_career_info(args.path)
    raw_table = man.create_table(df_country_info, df_career_info)
    country_dictionary = mac.get_country_dictionary()
    country_clean_dictionary = mwr.clean_country_dicctionary(country_dictionary)
    mwr.change_to_country_name(raw_table, country_clean_dictionary)
    chosen_country = input('Please choose a country: ')
    chosen_country_final = mwr.country_input(raw_table, chosen_country)
    print('please, be patient...the creation of job urls takes some time..')
    list_id = man.list_with_job_ids(df_career_info)
    list_path_jobs = man.path_jobs(list_id, args.job_path)
    job_name_uuid = mwr.get_json_data(list_path_jobs)
    job_dictionary = mwr.get_job_dictionary(job_name_uuid)
    print('get job data')
    mwr.change_to_job_name(raw_table, job_dictionary)
    print('change job codes to job names')
    print('change country codes to country names')
    print('clean the column area')
    mwr.clean_rural_column(raw_table)
    print('add the column -Quantity -')
    mwr.add_quantity_column(raw_table)
    grouped_table = mwr.group_raw_table(raw_table)
    mwr.add_percentage_column(grouped_table)
    print('add the column -Percentage -')
    mre.store_final_table(grouped_table)
    print('you can find the complete table as csv file in the results folder')
    country_df = mwr.choose_country(grouped_table, chosen_country_final)
    print(country_df)




if __name__ == '__main__':
    args = argument_parser()
    main(args)


