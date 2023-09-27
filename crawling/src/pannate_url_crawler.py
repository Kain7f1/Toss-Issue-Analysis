# pip install
############################################
# webdriver bs4 requests datetime pandas re #
############################################

# 안되시면 pycharm에서 진행해주세요!

# Library
# Crawling
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import requests

# time
import datetime
from datetime import datetime
import time
from calendar import monthrange

# pandas
import pandas as pd
import re

##################################################

# print("a")  # 수정사항


# Web Driver

def get_driver(url):
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('disable-gpu')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(url)
    return driver


# Func info: 네이트판 게시물 제목, url, media 갖고오는 함수
# input: keyword, max_pages(편의상 default를 500으로 두었음)
# Note: keyword로 검색한 내용을 500페이지까지 갖고오는 함수입니다.
def get_pann_url(keyword, max_pages=400):
    data = []
    #페이지처리:for문으로 처리
    for page_num in range(1, max_pages + 1):
        if page_num == 400:
            print("크롤링을 종료합니다.")
            break


        print(f"페이지 {page_num} 처리 중...")

        search_url = f'https://pann.nate.com/search/talk?searchType=A&q={keyword}&page={page_num}'
        response = requests.get(search_url)

        if response.status_code != 200:
            print(f"페이지 {page_num}를 가져오지 못했습니다. 상태 코드: {response.status_code}")
            continue

        soup = BeautifulSoup(response.content, 'html.parser')
        srch_result = soup.select(".srcharea a")

        for i, link in enumerate(srch_result):
            if 'title' in link.attrs:  # 'title' 속성이 있는 경우에만 딕셔너리에 넣어주기.
                title_text = link['title']
                clean_title_text = re.sub(r'\[.*?\]', '',title_text.strip())

                # "페이지"라는 텍스트가 title_text에 없을 경우만 처리
                if "페이지" not in title_text:
                    print(f"링크 {i + 1} 처리 중...")
                    row = {
                        'title': clean_title_text,
                        'url': 'https://pann.nate.com' + link['href'],
                        'media': 'pannate_teen'
                    }
                    data.append(row)  # 'row' 딕셔너리를 'data' 리스트에 추가



    df = pd.DataFrame(data)
    df.dropna(axis=0, inplace=True)
    df.to_csv('pannate_teen_url.csv', index=False, encoding='utf-8')


# 함수 호출 예시
get_pann_url("토스")