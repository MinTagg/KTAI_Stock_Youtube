import os

from crawling import get_summary_with_query
from embedding_automation import embedding
from visualizer import visualizer
from config import *
from file_editor import edit_config_file
from abstraction_automation import get_topics

def save_txt(path, language):
    # youtube_urls.txt 파일을 path로 이동
    with open('youtube_urls.txt', 'r') as f:
        data = f.read()
    try:
        os.mkdir(path)
    except:
        pass

    with open(path + f'youtube_urls_{language}.txt', 'w') as f:
        f.write(data)

base_path = 'DATA/' # 앞으로의 모든 데이터가 저장될 폴더
#sequence = [('Nvidia', ('엔비디아 분석', 'nvidia analysis')), ('tesla', ('테슬라 분석', 'tesla analysis')), ('amd', ('amd 분석', 'amd analysis'))] # 실행될 순서 (폴더 이름, (한글 검색어, 영어 검색어))
#sequence = [('tesla', ('테슬라 분석', 'tesla analysis')), ('amd', ('amd 분석', 'amd analysis'))] # 실행될 순서 (폴더 이름, (한글 검색어, 영어 검색어))
sequence = [('amd', ('amd 분석', 'amd analysis'))] # 실행될 순서 (폴더 이름, (한글 검색어, 영어 검색어))

NUM_OF_VIDEO = 10

base_folder = FOLDER_NAME
base_search = SEARCH_NAME

try:
    os.mkdir(base_path)
except:
    pass

for i, (new_folder_name, (new_search_name_kr, new_search_name_en)) in enumerate(sequence):
    print(f'{new_folder_name} start')

    # try to make base_path folder
    path = base_path + new_folder_name + '/'

    # 한글 시작
    # config.py 파일 수정
    edit_config_file(base_folder, base_search, new_folder_name, new_search_name_kr)# 폴더명, 검색어 변경
    base_folder = new_folder_name
    base_search = new_search_name_kr
    # 크롤링 시작
    state = True
    while state:
        try:
            get_summary_with_query(new_search_name_kr, NUM_OF_VIDEO)
            state = False
        except:
            continue
    # 요약 시작 -> run.sh 파일 실행
    os.system('sh run.sh')
    # 유튜브 링크 이동
    save_txt(path, 'kor')
    # 저장 파일 이동
    os.rename(f'{base_folder}_category',  path+f'data_{new_folder_name}_kor_category')

    # 영어 시작
    # config.py 파일 수정
    edit_config_file(base_folder, base_search, new_folder_name, new_search_name_en)# 폴더명, 검색어 변경
    # 크롤링 시작
    state = True
    while state:
        try:
            get_summary_with_query(new_search_name_en, NUM_OF_VIDEO)
            state = False
        except:
            continue
    # 요약 시작 -> run.sh 파일 실행
    os.system('sh run.sh')
    # 유튜브 링크 이동
    save_txt(path, 'us')
    # 저장 파일 이동
    os.rename(f'{base_folder}_category', path + f'data_{new_folder_name}_us_category')

    # 기업 임베딩 시작
    embedding(path, new_folder_name)
    # delete FOLDER_NAME folder
    os.system(f'rm -rf {new_folder_name}')


visualizer(base_path)


