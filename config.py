FOLDER_NAME = 'data' # 저장할 폴더의 이름 -> GPT거친 결과는 <FOLDER_NAME>_category에 pkl로 저장됨
SEARCH_NAME = 'Apple Stock' # 유튜브에 검색할 키워드
NUM_OF_VIDEO = 5 # 몇개의 비디오를 크롤링할지

SYSTEM_SCRIPT = 'Please ignore all previous instructions.Please respond only in the English language. Do not explain what you are doing. Do not self reference.You are an expert text analyst and researcher.Please extract and name the main topics and keywords from the text I provide.Please show the results with the following shape without bullet point or number.: <name of topic>/<keywords related to main topic>.'