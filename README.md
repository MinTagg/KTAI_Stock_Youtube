# 사용 전 설치

https://chromedriver.chromium.org/downloads 에서 크롬 드라이버 본인 컴퓨터 OS에 맞게 다운받고 .py폴더랑 같은 위치에 두기

잘 안되면 https://0433.tistory.com/40 참조


# 사용 전 세팅(MAC OS 기준)

1. 터미널
```bash
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222 --user-data-dir="/Users/<사용자이름>/Applications/Google Chrome.app/"
```
위 명령어 사용자 이름 변경해서 입력, 터미널 종료 금지

1-1. 명령어 안되면

```bash
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222 --user-data-dir="~/ChromeProfile"
```
2. 입력하면 크롬 창이 하나 자동으로 뜨는데 해당 크롬 창에서 미리 릴리스 로그인 해놓기 + 크롬 창 닫기 금지
-----

# 사용 전 세팅(WINDOW 기준)
1. 명령창
```bash
C:\Program Files (x86)\Google\Chrome\Application\chrome.exe --remote-debugging-port=9222 --user-data-dir="C:/ChromeTEMP"
```
1-1. 명령어 안되면
```bash
C:\Program Files\Google\Chrome\Application\chrome.exe --remote-debugging-port=9222 --user-data-dir="C:/ChromeTEMP"
```
2. 입력하면 크롬 창이 하나 자동으로 뜨는데 해당 크롬 창에서 미리 릴리스 로그인 해놓기 + 크롬 창 닫기 금지

-----

# Topic 추출 자동화
- OpenAI 설치

```bash
pip install openai
```

### OpenAI API키 생성 
- Create New Secret Key -> key 복사해두기(다시 못봄)

https://platform.openai.com/api-keys

### API 환경변수 설정

1.  Mac
    ```bash
    nano ~/.zshrc
    ```

    제일 밑에 추가

    ```bash
    export OPENAI_API_KEY='<API KEY 번호>'
    ```

    저장하고(cntl + O) 나가기 (cntl + x)

2. Windows

    시스템 환경 변수 편집 검색 -> 환경변수 -> 시스템 변수 -> 새로만들기 

    ```
    변수 이름 = OPENAI_API_KEY
    변수 값 = <API KEY 번호>
    ```

3. API 적용확인
    터미널/CMD 닫고 다시 킨 후에 확인하기
    mac : terminal
    ```
    echo $OPENAI_API_KEY
    ```
    windows : cmd
    ```
    echo %OPENAI_API_KEY%
    ```

https://platform.openai.com/docs/quickstart?context=python

----

# 저장 내용
릴리스에서 긁어 오는 것 = {config.folder_name}/*.txt

GPT로 뽑은 topic = {config.folder_name}_category/*.pkl

GPT로 뽑은 내용 전체 (topica/keywords) = {config.folder_name}_category/original/*.txt


### pkl 열기
```python
with open(<PATH_OF_FILE>, 'rb') as f:
    data = pkl.load(f)
```

# 전체 실행
main.py 파일 실행
# 사전 세팅
config.py에서 설정
# 기타 사항
릴리스에서 요약본 뽑을 때, 영어로 뽑는거 추천

계정설정 -> 내 언어 설정 -> 요약노트 언어 -> 영어

# 실행 방법 :: crawling.py만 실행하는 경우
## 1. 영상을 직접 선정해 요약본 뽑을 경우
        1. youtube_urls.txt 만들고 선정한 영상 링크 줄 단위로 입력
        2 main에서 get_summary_with_urls() 함수 실행
## 2. youtube에서 영상 자동으로 가져올 경우
        1. main에서 get_summary_with_query()함수 실행
        2. 인자는 query -> 유튜브에 검색할 검색어, video_nums -> 위에서부터 몇개 영상 가져올지
        3. 유튜브 필터 바꿔야될거 같으면 말해주세용. 이거 바꾸는것도 인자로 넣어서 자동화 하려면 할 수 있음...........
    

###########오류가 날 경우#########
다시 실행해보고 계속 같은 오류 나면 말해주세요....
