import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os

def saving(x, y, type_of_graph, company_name): # saving(x,y, 'mentioned_video', path)
    plt.bar(x, y[0], color='palevioletred', label='KOR')
    # mulpiply -1 to y[1] to show negative value
    plt.bar(x, y[1]*-1, color='steelblue', label='US')
    plt.legend()
    plt.xlabel('Affinity index')
    plt.ylabel(type_of_graph)
    plt.title(f'{company_name} {type_of_graph}')

    # try to make Visualization/{company_name} folder
    try:
        os.makedirs(f'Visualization/{company_name}')
    except:
        pass

    plt.savefig(f'Visualization/{company_name}/{type_of_graph}.png')
    plt.close()

def mentioned_video(dataframe):
    max_num = dataframe['num'].max()+1
    country_num = len(dataframe['country'].unique())
    x = np.arange(max_num)
    y = np.zeros((country_num, max_num))
    for i in range(max_num):
        for j in range(country_num):
            path = dataframe[(dataframe['num'] == i) & (dataframe['country'] == j)]['path']
            path = path.drop_duplicates()
            y[j][i] = len(path)

    return x, y

def mentioned_topic(dataframe):
    max_num = dataframe['num'].max()+1
    country_num = len(dataframe['country'].unique())
    x = np.arange(max_num)
    y = np.zeros((country_num, max_num))
    for i in range(max_num):
        for j in range(country_num):
            path = dataframe[(dataframe['num'] == i) & (dataframe['country'] == j)]['path']
            y[j][i] = len(path)

    return x, y

def mentioned_time(dataframe):
    max_num = dataframe['num'].max()+1
    country_num = len(dataframe['country'].unique())
    x = np.arange(max_num)
    y = np.zeros((country_num, max_num))
    for i in range(max_num):
        for j in range(country_num):
            times = dataframe[(dataframe['num'] == i) & (dataframe['country'] == j)]['time_weight']
            y[j][i] = sum(times)

    return x, y

def visualizer(base_path):
    company_csv_path = os.listdir(base_path)
    company_csv_path = [base_path+i for i in company_csv_path if i.endswith('.csv')]

    for path in company_csv_path:
        company_name = path.split('/')[-1].split('.')[0]
        df = pd.read_csv(path)
        x,y = mentioned_video(df)
        saving(x,y, 'mentioned_video', company_name)
        x,y = mentioned_topic(df)
        saving(x,y, 'mentioned_topic', company_name)
        x,y = mentioned_time(df)
        saving(x,y, 'mentioned_time', company_name)