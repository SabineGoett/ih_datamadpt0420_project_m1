import pandas as pd
from p_acquisition import m_acquisition as mac

# analysis functions



def create_table(df_country_info, df_career_info):
    merged_table = pd.merge(left = df_country_info, right= df_career_info, left_on = 'uuid', right_on = 'uuid')
    new_table = merged_table[['country_code', 'normalized_job_code', 'rural']]
    return new_table

def list_with_job_ids(job_code):
    list_ids = []
    l = job_code['normalized_job_code'].values.tolist()
    for x in l:
        if x != None:
            list_ids.append(x)
        s = set(list_ids)
        list_ids_unique = list(s)
    return list_ids_unique

def path_jobs(list_id, job_path):
    list_path_jobs = []
    for x in list_id:
        u = job_path + x
        list_path_jobs.append(u)
    return list_path_jobs