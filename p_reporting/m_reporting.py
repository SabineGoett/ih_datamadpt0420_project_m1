import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# reporting functions

def store_final_table(grouped_table):
    path_return = './data/results/final_job_table.csv'
    return grouped_table.to_csv(f'{path_return}', index=False)