from make_folder import *
import os

def edit_config_file(base_folder_name, base_search_name, new_folder_name, new_search_name):
    with open('config.py', 'r') as f:
        data = f.read()
    data = data.replace(base_search_name, new_search_name)
    data = data.replace(base_folder_name, new_folder_name)
    with open('config.py', 'w') as f:
        f.write(data)

new_names = ['Nvidia', 'Tesla', 'Apple', 'Microsoft', 'AMD']
new_search_names = ['Nvidia analysis', 'Tesla analysis', 'Apple analysis', 'Microsoft analysis', 'AMD analysis']
base_folder_name = FOLDER_NAME
base_search_name = SEARCH_NAME

for i, new_name in enumerate(new_names):
    new_folder_name = new_name
    new_search_name = new_search_names[i]
    edit_config_file(base_folder_name, base_search_name, new_folder_name, new_search_name)
    # run run.sh file
    os.system('sh run.sh')
    print(f'{new_name} folder is created')
    print(f'{new_name} folder is created in backup folder')
    print('-----------------------------------')
    base_folder_name = new_folder_name
    base_search_name = new_search_name