import os
import pickle as pkl
from openai import OpenAI
from config import *

def get_topics():
    file_paths = get_data_files(FOLDER_NAME)

    for file_path in file_paths:
        with open(file_path, 'r', encoding='utf-8') as f:
            contents = f.read()
            index = contents.find('완벽한 영상요약, 릴리스에이아이')
            response = gpt_call(contents[:index], SYSTEM_SCRIPT)
            
            if not os.path.exists(f'{FOLDER_NAME}_category'):
                os.mkdir(f'{FOLDER_NAME}_category')
            if not os.path.exists(f'{FOLDER_NAME}_category/original'):
                os.mkdir(f'{FOLDER_NAME}_category/original')
            
            with open(f'{FOLDER_NAME}_category/original/{file_path.split("/")[-1]}', 'w', encoding='utf-8') as f:
                f.write(response)
            with open(f'{FOLDER_NAME}_category/{file_path.split("/")[-1].split(".")[0]}.pkl', 'wb') as f:
                pkl.dump([x.split('/')[0] for x in response.split('\n')], f)

def get_data_files(folder_name):
    data_files = []
    for file_name in os.listdir(folder_name):
        if file_name.endswith('.txt') and file_name != 'total.txt':
            data_files.append(os.path.join(folder_name, file_name))
    return data_files

def gpt_call(contents, system_script, gpt = 'gpt-4-0613'):
    client = OpenAI()
    response = client.chat.completions.create(
    model=gpt,
    messages=[
        {
        "role": "system",
        'content': system_script
        #"content": "."
        },
        {
        "role": "user",
        "content": contents
        }
    ],
    temperature=0,
    max_tokens=1024,
    top_p=1)
    return response.choices[0].message.content