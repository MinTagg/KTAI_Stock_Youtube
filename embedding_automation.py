import os
from openai import OpenAI
from config import *
from tqdm import tqdm
import pandas as pd
from sklearn.cluster import AffinityPropagation
import numpy as np
from abstraction_automation import gpt_call
import pickle as pkl

def gpt_embedding_call(contents, gpt = 'text-embedding-3-large'):
    """
    contents: list of strings
    """
    client = OpenAI()
    response = client.embeddings.create(
    model=gpt,
    input = contents,
    )
    temp = []
    for i in response.data:
        temp.append(i.embedding)

    return temp

def path2emmbedding_without_time(path, country_code, dataframe=None):
    if dataframe is None:
        dataframe = pd.DataFrame(columns = ['country', 'topic', 'time_weight', 'num', 'New topic name from GPT', 'path', 'embeddings'])
    
    # list of pkl files in path
    pkl_list = os.listdir(path)
    pkl_list = [i for i in pkl_list if i.endswith('.pkl')]
    for pkl_name in tqdm(pkl_list):
        with open(path + pkl_name, 'rb') as f:
            contents = pkl.load(f)
        embeddings = gpt_embedding_call(contents)
        for i in range(len(embeddings)):
            dataframe = pd.concat([dataframe, pd.DataFrame([[country_code, contents[i], None, None, None, path + pkl_name, embeddings[i]]], columns = dataframe.columns)], ignore_index=True)
    return dataframe
    

def path2embedding(path, country_code, dataframe=None):
    """
    path: path to the txt file
    """
    if dataframe is None:
        dataframe = pd.DataFrame(columns = ['country', 'topic', 'time_weight', 'num', 'New topic name from GPT', 'path', 'embeddings'])
    # get the list of txt files
    for txt in tqdm(os.listdir(path)):
        time_list = []
        topic_list = []
        with open(path + txt, 'r') as f:
            lines = f.readlines()
            for line in lines:
                topic, time = line.strip().split('쳌')
                topic_list.append(topic)
                time_list.append(time)

        embeddings = gpt_embedding_call(topic_list) # 각 라인별로 embeddings 값
        for i in range(len(embeddings)):
            dataframe = pd.concat([dataframe, pd.DataFrame([[country_code, topic_list[i], time_list[i], None, None, path + txt, embeddings[i]]], columns = dataframe.columns)], ignore_index=True)
            
    return dataframe

def get_embedding(base_path, company_name, country = {'kor':0, 'us':1}):
    dataframe = pd.DataFrame(columns = ['country', 'topic', 'time_weight', 'num', 'New topic name from GPT', 'path', 'embeddings'])
    for i in range(len(country)):
        print(f'{list(country.keys())[i]} start')
        dataframe = path2embedding(f'{base_path}data_{company_name}_{list(country.keys())[i]}_category/', list(country.values())[i], dataframe)
    return dataframe

"""
def aff_cluster(dataframe):

1. get embeddings from dataframe
2. fit the embeddings with affinity_propagation
3. get the cluster_centers_indices
"""

def aff_cluster(dataframe):
    embeddings = np.array(dataframe['embeddings'])
    embeddings = np.array([np.array(i) for i in embeddings])

    labels = AffinityPropagation(random_state=5).fit(embeddings)
    return labels

"""
def clustering(dataframe):

1. get the cluster_centers_indices from aff_cluster
2. set the cluster_centers_indices to dataframe['num']
3. return dataframe
"""

def clustering(dataframe):
    labels = aff_cluster(dataframe)
    dataframe['num'] = labels.labels_
    # sort by country
    dataframe = dataframe.sort_values(by='country')
    # sort by num
    dataframe = dataframe.sort_values(by='num')
    max_num = dataframe['num'].max()
    """get new topic using gpt_call
    1. get all the topics that have the same num
    2. make it into one string
    3. call gpt_call
        system_script = NEWTOPIC_PROMPT
        contents = the string
    4. set the new topic to dataframe that has the same num
    """

    for i in range(max_num+1):
        temp = dataframe[dataframe['num'] == i]
        temp = temp['topic'].tolist()
        temp = ', '.join(temp)
        new_topic = gpt_call(temp, NEWTOPIC_PROMPT)
        dataframe.loc[dataframe['num'] == i, 'New topic name from GPT'] = new_topic
    return dataframe

def embedding(base_path, company_name):
    dataframe = get_embedding(base_path, company_name)
    dataframe = clustering(dataframe)

    # for without visualization - delete 'embeddings' column
    #dataframe = dataframe.drop('embeddings', axis=1)
    
    dataframe.to_csv(f'{base_path[:-1]}.csv', index=False)
