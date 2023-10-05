# Made by Hansol Lee 20230925

from crawling_tool import get_gall_id, get_url_base, get_max_num, get_last_page
from bs4 import BeautifulSoup
import utility_module as util
import requests
import pandas as pd
import re

# keyword = "토스"
# 2015-02-26 ~
header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
    }


##############################################
# 목적 : 디시인사이드 글 url 받아오기
# 입력값 : 입력 키워드(토스), 갤러리 id
# 리턴 : x
# 생성 파일 : url_dcinside_{gall_id}.csv
# columns = ['date', 'title', 'url', 'media']
def get_url_dcinside(gall_url, keyword):
    # 0. 기본값 세팅 단계
    try:
        gall_id = get_gall_id(gall_url)                     # 갤러리 id
        url_base = get_url_base(gall_url)                   # "https" 부터 "board/" 이전까지의 url 부분 (major갤, minor갤, mini갤)
        max_num = get_max_num(keyword, gall_id, url_base)   # 검색결과 중, 가장 큰 글번호 10000단위로 올림한 값/10000
        print(url_base)
        print(gall_id)
        print(max_num)
        folder_path = f"./url/{gall_id}"        # 저장할 폴더 경로 설정
        util.create_folder(folder_path)         # 폴더 만들기
        error_log = []                          # 에러 로그 저장
        data_list = []                          # 데이터 리스트 ['date', 'title', 'url', 'media']
        file_name = f"url_{gall_id}"            # 저장할 파일 이름
        url = '_'
        temp_url = '_'
        search_url = '_'
    except Exception as e:
        print("[기본값 세팅 단계에서 error가 발생함] ", e)
        print("[get_url_dcinside() 종료]")
        return 0

    # 1. url 크롤링
    for search_pos in range(max_num, 0, -10000):
        try:
            print(f"[1만 개 단위로 검색합니다. 검색어 : {keyword} ] " + "*"*100)
            print(f"[search_pos : {search_pos}] " + "*"*114)
            temp_url = f"{url_base}/board/lists/?id={gall_id}&page=1&search_pos=-{search_pos}&s_type=search_subject_memo&s_keyword={keyword}"
            last_page = get_last_page(temp_url)     # 1만 단위 검색결과의 마지막 페이지
        except Exception as e:
            step = "[url 크롤링]"
            print(f'[error]{step}[error message : {e}]')
            error_log.append([temp_url, step, e])
            continue
        # 해외주식갤러리처럼 컨텐츠 많을때, 1,2,3,4,5 이렇게 페이징 되어있는거 있음. 이걸 페이지 넘기면서 크롤링
        for page in range(1, last_page+1):
            try:
                # [검색결과 페이지 불러오기]
                print(f"[크롤링 시작][search_pos : {search_pos}][page : {page}/{last_page}]")
                search_url = f"{url_base}/board/lists/?id={gall_id}&page={page}&search_pos=-{search_pos}&s_type=search_subject_memo&s_keyword={keyword}"
                response = requests.get(search_url, headers=header)
                soup = BeautifulSoup(response.text, "html.parser")      # 검색 결과 페이지
                element_list = soup.select("table.gall_list tr.ub-content")     # 한 페이지 전체 글 리스트
                print(f"[글 개수 : {len(element_list)}]")
            except Exception as e:
                step = "[검색결과 페이지 불러오기]"
                print(f'[error]{step}[error message : {e}]')
                error_log.append([search_url, step, e])
                continue
            # 글 하나씩 뽑아서 크롤링
            for element in element_list:    # element == 글 하나
                try:
                    # [검색결과에서 글 하나씩 크롤링]
                    if element.find('td', class_='gall_writer').get_text() == "운영자":   # 페이지마다 광고글 처리하기
                        continue    # 광고글은 무시하고 넘어가기
                    date = element.find('td', class_='gall_date')['title'][:10]
                    title = util.preprocess_title(element.find('td', class_='gall_tit ub-word').find('a').get_text(strip=True))
                    url = "https://gall.dcinside.com" + element.select_one("td.gall_tit a")['href']
                    new_row = [date, title, url, gall_id]
                    data_list.append(new_row)  # data_list에 크롤링한 정보 저장
                    print(f"[page : {page}/{last_page}] new_row : {new_row}")
                except Exception as e:
                    step = "[검색결과에서 글 하나씩 크롤링]"
                    print(f'[error]{step}[error message : {e}]')
                    error_log.append([url, step, e])
                    continue

    # 2. 파일로 저장
    try:
        df_result = pd.DataFrame(data_list, columns=['date', 'title', 'url', 'media'])
        util.save_file(df_result, folder_path, f"{file_name}.csv")
    except Exception as e:
        step = "[파일 저장]"
        print('[error] ', e)
        error_log.append([url, step, e])

    # 3. 에러로그확인
    try:
        util.error_check(error_log, folder_path, file_name)
    except Exception as e:
        print('[error] ', e)
