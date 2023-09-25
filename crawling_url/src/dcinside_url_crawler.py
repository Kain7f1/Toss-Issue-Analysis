# Made by Hansol Lee 20230925

from utility_module import create_folder, error_check

from bs4 import BeautifulSoup
import pandas as pd
import requests
import os

# keyword = "토스"
# start_date = 2015-02-26
# end_date = 2023-09-19


# 목적 : 글 url 받아오기 - 토스 갤러리
# 입력값 : 입력 키워드(토스), 시작 날짜(20150226), 종료 날짜(20230919)
# 리턴 : x
# 생성 파일 : dcinside_toss_url.csv
# columns = ['date', 'title', 'url', 'media']

def get_url_dc_toss(keyword, start_date, end_date):
    media = "dcinside_toss"  # 토스 갤러리 media column
    header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"}
    folder_path = f"./{media}/url"  # 저장할 폴더 경로 설정
    create_folder(folder_path)      # 폴더 만들기
    error_log = []                  # 에러 로그 저장 [’date’, ’error’]
    data_list = []                  # 데이터 리스트 ['date', 'title', 'url', 'media']
    file_name = f"{media}_url"     # 저장할 파일 이름
    count_pinned_post = 3


    gall_url = "https://gall.dcinside.com/mgallery/board/lists/?id=toss"
    for page in range(12):
        try:
            search_url = f"https://gall.dcinside.com/mgallery/board/lists/?id=toss&page={page}"
            response = requests.get(search_url, headers=header)
            soup = BeautifulSoup(response.text, "html.parser")  # 페이지의 soup
            soup_box = soup.select("article")[1]  # 50개 게시글 있는 박스 soup
            element_list = soup.select("tbody tr")[count_pinned_post:]  # 한 페이지 전체 글 리스트
            print(len(element_list))    # 임시
            for element in element_list:
                td_list = element.select("td")  # element의 요소들 리스트

                date = td_list[4]['title']
                title = td_list[2].get_text(strip=True)
                url = "gall.dcinside.com" + td_list[2].find('a')['href']
                data_list.append([date, title, url, media])
                print([date, title, url, media])
        except Exception as e:
            print('[error occured] ', e)
            break

    # error_check(error_log, folder_path, file_name)















