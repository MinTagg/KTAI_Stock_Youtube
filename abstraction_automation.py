import os
import pickle as pkl
from openai import OpenAI
from config import *
from tqdm import tqdm

def get_topics():
    file_paths = get_data_files(FOLDER_NAME)

    for i, file_path in enumerate(file_paths):
        print(f"{i+1} start :: {file_path}")
        with open(file_path, 'r', encoding='utf-8') as f:
            contents = f.read()
        index = contents.find('완벽한 영상요약, 릴리스에이아이') # 뒤쪽 릴리스 광고 삭제
        contents = contents[:index].replace('   ', '').split('\n\n') # 뒤쪽 릴리스 광고 삭제 + 의미없는 띄어쓰기 삭제 + 문단별로 나눠서 리스트로 저장
        if len(contents) == 1: # 문단이 하나인 경우, 문장별로 나눠서 리스트로 저장
            pass
        else:
            contents = contents[:-1]
        # filter 함수를 통해 관련있는 문단만 추출
        # TODO: debugging_history 출력 방법 추가하기 -> log에 저장하거나, 따로 파일로 저장하기
        #if FILTER_DEBUGGING:
        #    contents, debugging_history = filter(contents, debug = FILTER_DEBUGGING)
        #else:
        #    contents = filter(contents, debug = FILTER_DEBUGGING)
        # gpt_call 함수를 통해 문단을 카테고리로 분류
        
        ## without filter
        # gather all contents(list)

        contents = '\n'.join(contents)

        response = gpt_call(contents, SYSTEM_SCRIPT)
        # 파일 저장을 위한 폴더 생성
        make_folder()
        
        with open(f'{FOLDER_NAME}_category/original/{file_path.split("/")[-1]}', 'w', encoding='utf-8') as f: # txt파일 저장
            f.write(response)
        with open(f'{FOLDER_NAME}_category/{file_path.split("/")[-1].split(".")[0]}.pkl', 'wb') as f: # pkl파일 저장
            pkl.dump([x.split('/')[0] for x in response.split('\n')], f)

def make_folder():
    if not os.path.exists(f'{FOLDER_NAME}_category'):
        os.mkdir(f'{FOLDER_NAME}_category')
    if not os.path.exists(f'{FOLDER_NAME}_category/original'):
        os.mkdir(f'{FOLDER_NAME}_category/original')

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

def filter(contents, debug = False):
    temp_context = contents[0] # 첫번째 제목을 context로 설정
    if debug:
        debugging_history = ''
    for i in tqdm(range(1, len(contents))):
    #for i in range(1, len(contents)): # 한 문단씩 읽어가면서 context와 주제를 바탕으로 관련있는지 확인
        gpt_input = f"<Main topic>: {SEARCH_NAME}\n<Context>: {temp_context}\n<Target>: {contents[i]}"
        response = gpt_call(contents= gpt_input, system_script= FILTER_PROMPT)
        if 'True' in response: # 관련이 있는 경우 context에 추가
            temp_context += '\n' + contents[i]
        elif 'False' in response and debug: # 관련이 없는 경우 디버깅 히스토리에 추가
            debugging_history += f"{contents[i]}\n"
    if debug:
        return temp_context, debugging_history
    return temp_context