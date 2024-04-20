from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import os
import config

def open_lilys():
    headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'}
    lilys_address = "https://lilys.ai"
    a1 = "https://lilys.ai/digest/399723?videoId=MnApSQxDjis&result=summaryNote&source=video" # 실험용 url. 무시해도 됨.
    
    options = Options()
    options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    
    global driver
    driver = webdriver.Chrome(options = options) # 디버깅 모드 -> 로그인 생략
    driver.get(lilys_address) 
    try: # 서버 점검과 같은 공지사항 창 시작시 뜨는 경우 확인 클릭
        driver.find_element(By.CSS_SELECTOR,'body > div > div.simpleModalWrapper > div.simpleModal > div.simpleModalButtonWrapper > div').click()
    except:
        pass

def delete_banner():
    try:
        time.sleep(1)
        driver.find_element(By.CSS_SELECTOR, 'body > div > div.topBanner.promotion > div.topBannerClosebutton').click()
        print('banner 지움')
    except:
        pass
    
def give_url(url):
    if len(url) < 5:
        return
    delete_banner()
    elem = driver.find_element(By.CSS_SELECTOR, 'body > div > div.App.video.isSidebarFolded > div.mainWrapper > div.infoConverter > div.infoConverterBody > div.digestSection > div.inputSection > div.sourceInputWrapper > div.sourceInput.video > div.inputs > input')
    elem.clear()
    elem.send_keys(url)
    driver.find_element(By.CSS_SELECTOR, 'body > div > div.App.video.isSidebarFolded > div.mainWrapper > div.infoConverter > div.infoConverterBody > div.digestSection > div.inputSection > div.sourceInputWrapper > div.sourceInput.video > div.confirmButtonSection > div').click()

def get_summary_script(file_name): #사이드바 접음
    delete_banner()
    def script():
        os.makedirs(config.FOLDER_NAME, exist_ok=True)
        out_file = os.path.join(config.FOLDER_NAME, file_name + '.txt')
        f = open(out_file, "w+")
        time.sleep(2)
        driver.find_element(By.CSS_SELECTOR, 'body > div > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(4) > div:nth-child(2) > div:nth-child(1) > div:nth-child(3)').click()
        head_selector = 'body > div > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(4) > div:nth-child(3) > div '
        idx = 3
        chk = driver.find_element(By.CSS_SELECTOR, head_selector)
        while True:
            try:
                selector = head_selector + ' > div:nth-child({})'.format(idx)
                title_selector = selector + ' > div > div > div.titleSection > div.titleText'
                title = driver.find_element(By.CSS_SELECTOR, title_selector).text
                title = title[32:]
                f.write(title+'\n')
                text_head_selector = selector + ' > div > div > div.chunksumContents > ul'
                textidx = 1
                while True:
                    try:
                        text_selector = text_head_selector + ' > li:nth-child({})'.format(textidx) + ' > div'
                        text = driver.find_element(By.CSS_SELECTOR, text_selector).text
                        f.write(text+'\n')
                        textidx+=1
                    except:
                        f.write('\n')
                        break
                idx+=1
            except:
                break
        f.close()
    idx = 1
    while True: # 릴리스 로딩 고려
        try:
            script() #릴리스 로딩 완료
            return
        except:
            print('loading...', idx)
            idx+=1
            time.sleep(5) # 릴리스 로딩 중

def get_full_script(file_name):
    delete_banner()
    def script():
        out_file = file_name+'.txt'
        f = open(out_file, "w+")
        time.sleep(2) # 혹시 오류나면 숫자 늘리기
        driver.find_element(By.CSS_SELECTOR, 'body > div > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(4) > div:nth-child(1) > div:nth-child(2) > div').click()
        head_selector = 'body > div > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(4) > div:nth-child(3) > div:nth-child(1)'
        idx = 1
        chk = driver.find_element(By.CSS_SELECTOR, head_selector) # 로딩이 안됐다면 여기서 오류가 뜬다.
        while True:
            try:
                selector = head_selector + ' > div:nth-child({})'.format(idx) + ' > div.eachRawScript'
                t = driver.find_element(By.CSS_SELECTOR, selector).text
                f.write(t+'\n')
                idx += 1
            except:
                break
        f.close()
    while True: # 릴리스 로딩 고려
        try:
            script() #릴리스 로딩 완료
            return
        except:
            print('loading...')
            time.sleep(5) # 릴리스 로딩 중
     
def go_to_home():
    driver.find_element(By.CSS_SELECTOR, 'body > div > div:nth-child(1) > div:nth-child(1) > div:nth-child(1)').click() 
    driver.find_element(By.CSS_SELECTOR, 'body > div > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(3)').click() 
    
def open_youtube():
    headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'}
    youtube_address = "https://www.youtube.com"
    
    options = Options()
    options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    
    global driver
    driver = webdriver.Chrome(options = options) # 디버깅 모드 -> 로그인 생략
    driver.get(youtube_address) 
    
def search(search_key):
    elem = driver.find_element(By.NAME, 'search_query')
    elem.clear()
    elem.send_keys(search_key)
    driver.find_element(By.ID, 'search-icon-legacy').click()
    
    time.sleep(1)
    driver.find_element(By.ID, 'filter-button').click() #이번주
    time.sleep(1)
    filter = driver.find_element(By.ID, 'options')
    filter.find_element(By.CSS_SELECTOR,'ytd-search-filter-group-renderer:nth-child(1) > ytd-search-filter-renderer:nth-child(6) > a > div').click()
    
    time.sleep(1)
    driver.find_element(By.ID, 'filter-button').click() #4분 ~ 20분
    time.sleep(1)
    filter = driver.find_element(By.ID, 'options')
    filter.find_element(By.CSS_SELECTOR,'ytd-search-filter-group-renderer:nth-child(3) > ytd-search-filter-renderer:nth-child(4) > a > div').click()
    
    time.sleep(1)
    driver.find_element(By.ID, 'filter-button').click() #조회수
    time.sleep(1)
    filter = driver.find_element(By.ID, 'options')
    filter.find_element(By.CSS_SELECTOR,'ytd-search-filter-group-renderer:nth-child(5) > ytd-search-filter-renderer:nth-child(6) > a > div').click()
    time.sleep(2)

def save_urls(save_num = 10):
    time.sleep(1)
    f = open('youtube_urls.txt', 'w+')

    primary = driver.find_element(By.CSS_SELECTOR, 'body > ytd-app > div.style-scope.ytd-app > ytd-page-manager > ytd-search > div:nth-child(1) > ytd-two-column-search-results-renderer > div')
    content = primary.find_element(By.CSS_SELECTOR, 'ytd-section-list-renderer > div:nth-child(2)')
    cnt = 0
    set_idx = 1
    while True:
        try:
            video_set = content.find_element(By.CSS_SELECTOR, 'ytd-item-section-renderer:nth-child({})'.format(set_idx) + ' > div:nth-child(3)')
            video_idx = 1
            while True:
                try:
                    video = video_set.find_element(By.CSS_SELECTOR, 'ytd-video-renderer:nth-child({})'.format(video_idx))
                    url_info = video.find_element(By.CSS_SELECTOR, 'div:nth-child(1) > ytd-thumbnail > a')
                    url = url_info.get_attribute('href')
                    #print(url)
                    f.write(url+'\n')
                    cnt += 1
                    video_idx+=1
                    if cnt == save_num:
                        print("{}개의 동영상 url 저장 완료.".format(cnt))
                        return
                except:
                    break
            set_idx+=1
            body = driver.find_element(By.CSS_SELECTOR, 'body')
            for _ in range(30):
                body.send_keys(Keys.PAGE_DOWN)
            time.sleep(1)
        except:
            print("영상 url 저장 실패. {}개의 url 저장했습니다. 영상이 {}개 만큼 없을 수 있습니다.".format(cnt, save_num))
            break

def get_summary_with_urls():
    fp = open('youtube_urls.txt', 'r')
    for idx, url in enumerate(fp):
        url = url[:-1]
        open_lilys()
        give_url(url)
        get_summary_script(str(idx+1)) 

def get_summary_with_query(query, video_nums):
    open_youtube()
    search(query)
    save_urls(video_nums)
    fp = open('youtube_urls.txt', 'r')
    for idx, url in enumerate(fp):
        url = url[:-1]
        open_lilys()
        give_url(url)
        get_summary_script(str(idx+1))   
        
if __name__ == "__main__":
    ('apple stock', 5)
    #get_summary_with_urls()