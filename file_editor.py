def edit_config_file(base_folder_name, base_search_name, new_folder_name, new_search_name):
    with open('config.py', 'r') as f:
        data = f.read()
    data = data.replace(base_search_name, new_search_name)
    data = data.replace(base_folder_name, new_folder_name)
    with open('config.py', 'w') as f:
        f.write(data)
