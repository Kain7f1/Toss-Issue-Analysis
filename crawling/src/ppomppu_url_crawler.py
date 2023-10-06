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


#func info: 뽐뿌 게시글의 제목, 게시날짜, url을 갖고옵니다.
#input: id(게시판), keyword(검색어)
#id info
# 자유게시판 = freeboard (703page)
# 재태크포럼 = money (307page)
# 증권포럼 = stock (44page)
#output: 해당 게시판에 있는 게시글의 date, title, url이 있는 df가 만들어집니다.
# 파일이름: ppomppu_{id}_url.csv


def get_ppomppu_url(id, keyword, max_pages=40000):
    data_list = []

    for page_num in range(0, max_pages + 1):
        if page_num == 328:
            print("크롤링을 종료합니다.")
            break
        print(f"페이지 {page_num} 처리 중...")

        search_url = f'https://www.ppomppu.co.kr/zboard/zboard.php?id={id}&page={page_num}&search_type=sub_memo&keyword={keyword}&divpage=1584'
        response = requests.get(search_url)

        if response.status_code != 200:
            print(f"페이지 {page_num}를 가져오지 못했습니다. 상태 코드: {response.status_code}")
            continue

        soup = BeautifulSoup(response.content, 'html.parser')


        # tr 태그안에 있는 title,date, url 정보를 긁어옵니다
        tr_tags = soup.find_all('tr')

        for tr in tr_tags:
            title_tag = tr.find('font', class_='list_title')
            date_tag = tr.find('nobr', class_='eng list_vspace')

            if title_tag and title_tag.parent.name == 'a':
                url = 'https://www.ppomppu.co.kr/zboard/' + title_tag.parent['href']

                if ":" in date_tag.text:
                    date = "2023-10-06"
                    # Note: 오늘 날짜에 게시된 글의 경우 hh:mm와 같이 시간에 :가 들어감
                    # datetime활용 필요있음 - 계속적인 오류로 임시적으로 처리함
                else:
                    date = "20" + date_tag.text.replace('/', '-')
                    # Note: 뽐뿌의 날짜형식: %y-%m-%d
                    # %Y-%m-%d 형식으로 바꾸어줌

                title = title_tag.text.strip().replace(',', '')

                # Note: url에 //zboard/가 들어가있거나, http://s.ppomppu.co.kr? 로 시작하는 url은 광고성 글이여서 빼줌
                if url and "//zboard/" not in url and "http://s.ppomppu.co.kr?" not in url:
                    media = 'ppomppu'
                    data_list.append({
                        'date': date,
                        'title': title,
                        'url': url,
                        'media': media
                    })

    #데이터프레임 만들기
    df = pd.DataFrame(data_list, columns=['date', 'title', 'url', 'media'])
    df.to_csv(f"ppomppu_{id}_url_crawling.csv", index=False)

    return data_list


get_ppomppu_url('money', '토스', 328)