# 라이브러리
import pandas as pd
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

import re
import time


# Func info: url에서 url의 component를 뽑아냅니다
# input: csv파일로 만든 url_list를 넣어줍니다
# output: {media}_content_crawling.csv를 만들어줍니다.
# columns: [date, title, url, media, contents, is_comment]


#############################
# get_driver()
# 기능 : driver를 반환합니다
# 리턴값 : driver
# 사용법 : driver = get_driver() 쓰고 driver.get(url) 처럼 사용합니다
def extract_components_from_urls(url_list):
    data_list = []
    date = ''
    title = ''
    url = ''
    media = ''
    content = ''
    is_comment_main_text = ''

    CHROME_DRIVER_PATH = "C:/Users/chromedriver.exe"    # (절대경로) Users 폴더에 chromedriver.exe를 설치했음
    # driver 설정
    options = webdriver.ChromeOptions()                 # (옵션)
    # options.add_argument("--start-maximized")         # 창이 최대화 되도록 열리게 한다.
    options.add_argument("headless")                    # 창이 없이 크롬이 실행이 되도록 만든다
    options.add_argument("disable-gpu")                 # 크롤링 실행시 GPU를 사용하지 않게
    options.add_argument("disable-infobars")            # 안내바가 없이 열리게 한다.한다.
    options.add_argument("--disable-dev-shm-usage")     # 공유메모리를 사용하지 않는다
    options.add_argument("--disable-extensions")        # 확장팩을 사용하지 않는다.
    driver = webdriver.Chrome(CHROME_DRIVER_PATH, options=options)


    try:
        for url in url_list:
            response = requests.get(url)
            time.sleep(1)
            if response.status_code != 200:
                print(f"Failed to get {url}")
                continue
            soup = BeautifulSoup(response.text, 'html.parser')

            #브라우저 옵션 설정

            driver = webdriver.Chrome(options=options)

            # 본문  ['date', 'title', 'url', 'media', 'contents', 'is_comment']
            # date 갖고오기
            target_div_date = soup.find('div', {'class': 'info'})
            if target_div_date:
                date_tag = target_div_date.find('span', {'class': 'date'})
                if date_tag:
                    print(f"{url}의 본문 작성일: {date_tag.text[:10].replace('.', '-')}")
                    date = date_tag.text[:10].replace('.', '-')

            # title 갖고오기
            target_div = soup.find('div', {'class': 'post-tit-info'})
            if target_div:
                h1_tag = target_div.find('h1')
                if h1_tag:
                    print(f"{url}의 컨텐츠 내용: {h1_tag.text}")
                    title = h1_tag.text.strip()

            # Url, media
            url = f"{url}"
            media = "pannate_teen"

            # content 갖고오기
            target_div_content = soup.find('div', {'id': 'contentArea'})
            if target_div_content:
                content = target_div_content.text.strip().replace('\n','')
                print("content:", content)
                # is_comment에 추가
                # 본문:0, 댓글:1
                is_comment_main_text = "0"
                print("본문이면 0, 댓글이면 1로 라벨링 :", is_comment_main_text)

            #내용을 data_list에 넣어준다
            data_list.append([date, title, url, media,content, is_comment_main_text])
            print(data_list)



            #####################################################

            # 댓글 갖고오기
            # 댓글의 date 가져오기
            dt_tags = soup.find_all('dt')
            for dt in dt_tags:
                i_tag = dt.find('i')
                if i_tag:
                    print(f"{url}에 달린 댓글 작성일:",i_tag.text[:10].replace('.', '-'))
                    date = i_tag.text[:10].replace('.', '-')

            # 댓글 컨텐츠
            pattern = re.compile('content_area_\d{8}')
            # 정규식표현으로 댓글태그 형식 지정
            # Note: 네이트판과 같은경우 댓글 태그는 contentArea뒤에 랜덤으로 8자리 숫자가 붙는다
            target_div_replys = soup.find_all('dd', {'id': pattern})

            if target_div_replys:  # 리스트가 비어있지 않을 경우만 실행
                for target_div_reply in target_div_replys:
                    content = target_div_reply.text.strip()

                    #삭제된 댓글입니다 처리: "삭제된" 이 포함된 문구는 건너뛰기
                    if re.search(r"삭제된",content):
                        continue

                    media = "pannate_teen"
                    is_comment_main_text = "1"

                    print(f"{url}에 달린 댓글내용:", content.strip().replace('\n', ''))
                    print("본문이면 0, 댓글이면 1로 라벨링 :", is_comment_main_text)

                    if target_div:
                        h1_tag = target_div.find('h1')
                        if h1_tag:
                            title = h1_tag.text.strip()
                            url = f"{url}"

                    data_list.append(
                        [date, title, url, media, content, is_comment_main_text])
                    print(data_list)
            else:
                print("이 글에는 댓글이 없습니다")


    except Exception as e:
        print('Error Occurs!', e)
        return []

    df_result = pd.DataFrame(data_list, columns=['date', 'title', 'url', 'media', 'contents', 'is_comment'])
    # df: 판네이트 url 크롤링한 데이터의 df가 할당됨
    # df_result: 위 코드를 통해 만들어진 df

    df_result.to_csv('pannate_content_crawling.csv', index=False)

# CSV 파일에서 url 읽어오기
df = pd.read_csv('pannate_teen_url.csv')
urls = df['url'].tolist()

# 함수 실행
extract_components_from_urls(urls)

