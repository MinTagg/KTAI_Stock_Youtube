from abstraction_automation import get_topics
from crawling import get_summary_with_query
from config import *

if __name__ == '__main__':
    get_summary_with_query(SEARCH_NAME, NUM_OF_VIDEO)
    get_topics()