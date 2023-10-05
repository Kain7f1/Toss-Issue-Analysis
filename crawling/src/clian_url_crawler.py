# Library
# Crawling

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

res = requests.get(url)
soup = BeautifulSoup(res.text, "html.parser")

def get_clian_url(keyword, max_pages=400):
    data_list = []
    date = ''
    title = ''
    url = ''
    media = 'clian'

    #페이지처리:for문으로 처리
    for page_num in range(0, max_pages + 1):
        if page_num == 49:
            print("크롤링을 종료합니다.")
            break
        print(f"페이지 {page_num} 처리 중...")

        search_url = f'https://www.clien.net/service/search?q={keyword}&sort=recency&p={page_num}&boardCd=&isBoard=false'
        response = requests.get(search_url)

        if response.status_code != 200:
            print(f"페이지 {page_num}를 가져오지 못했습니다. 상태 코드: {response.status_code}")
            continue

        soup = BeautifulSoup(response.content, 'html.parser')

        # 모든 date와 title 가져오기
        date_tags = soup.find_all('span', class_='timestamp')
        a_tags = soup.find_all('a', class_='subject_fixed')

        # 각 타이틀 및 날짜에 대한 처리
        # Note: 지름(jirum)카테고리 - 알뜰구매 관련은 제외- 토스 기능에 대한 내용이 아닌, 토스로 할인 받아서 샀다는 것이 전부.
        # 필요없는 데이터라 판단하여 제거
        for date_tag, a_tag in zip(date_tags, a_tags):
            if 'jirum' in a_tag['href']:
              continue
            date = date_tag.text[:10]
            date_obj = datetime.strptime(date, "%Y-%m-%d")

            # Note: 토스 출시일 이전의 글을 제외하기 위해 datetime으로 비교처리
            if date_obj <= datetime.strptime("2015-02-26", "%Y-%m-%d"):
                print("2015-02-26 이전의 데이터입니다. 크롤링을 종료합니다.")
                break

            title = a_tag['title']
            url = "https://www.clien.net" + a_tag['href']

            print("link 내용:", url)
            print("title:", title)

            data_list.append([date, title, url, media])

    # 결과값 dataframe에 넣기
    df = pd.DataFrame(data_list, columns=['date', 'title', 'url', 'media'])
    df.to_csv('clian_url_crawling.csv', index=False)

    return data_list

get_clian_url('토스')



