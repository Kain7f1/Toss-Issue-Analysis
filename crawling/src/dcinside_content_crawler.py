#############################
# Made by Hansol Lee
# 20230927
#############################

from crawling_tool import get_gall_id, get_driver
import utility_module as util
import requests
import pandas as pd
import time
import datetime
from bs4 import BeautifulSoup


header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
    }


#####################################
# 본문에서 new_row를 얻어오는 함수
def get_new_row_from_main_content(time_sleep_sec, url_row):
    is_comment = 0  # 본문이므로 0
    response = requests.get(url_row['url'], headers=header)
    time.sleep(time_sleep_sec)
    soup = BeautifulSoup(response.text, "html.parser")
    content = util.preprocess_content_dc(soup.find('div', {"class": "write_div"}).text)
    content = url_row['title'] + " " + content
    new_row = [url_row['date'], url_row['title'], url_row['url'], url_row['media'], content, is_comment]
    return new_row


#####################################
# 기능 : url을 받아 reply_list를 리턴합니다
# 리턴값 : reply_list
def get_reply_list(time_sleep_sec, url):
    driver = get_driver()
    driver.get(url)
    time.sleep(time_sleep_sec)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    reply_list = soup.find_all("li", {"class": "ub-content"})
    return reply_list


#####################################
# 기능 : 댓글 html코드를 받아서, 댓글의 date를 리턴합니다
# 리턴값 : 2023-10-06 형식의 문자열
def get_reply_date(reply):
    now_year = str(datetime.datetime.now().year)
    temp_date = reply.find("span", {"class": "date_time"}).text.replace(".", "-")  # 댓글 등록 날짜 추출
    if temp_date[:2] == "20":  # 작년 이전은 "2022.09.07 10:10:54" 형식임
        date = temp_date[:10]
    else:  # 올해는 "09.30 10:10:54" 형식임
        date = str(datetime.datetime.now().year) + "-" + temp_date[:5]  # 올해 년도를 추가함
    return date


#####################################
# 기능 : 무시해야하는 댓글이면, True를 반환하고, 필요한 댓글이면 False를 반환합니다
def is_ignore_reply(reply):
    if reply.select_one("p.del_reply"):
        print("[삭제된 코멘트입니다]")
        return True
    elif reply.find('span', {'data-nick': '댓글돌이'}):
        print("[댓글돌이는 무시합니다]")
        return True
    elif reply.find('div', {'class': 'comment_dccon'}):
        print("[디시콘은 무시합니다]")
        return True
    else:
        return False

#####################################
# get_content()
# 목적 : url.csv를 읽어오고, 각 페이지의 정보를 추출하여 저장한다
# 입력값 : media
# 리턴값 : 없음
# 생성 파일 : content_dcinside_toss.csv
# columns = ['date', 'title', 'url', 'media', 'content', 'is_comment']
#################################
# [함수 진행]
# 1) url.csv를 df로 읽어옴
# 2-a) df에서 한 row 읽어옴
# 2-b) 본문 정보 row를 data_list에 추가
# 2-c) 댓글들 정보 row를 data_list에 추가
# 3-a) 다 끝났으면 다음 row 읽어옴
# 3-b) 2,3 반복
# 4) 끝나면 파일로 저장
# 5) 에러로그 체크 및 저장
#################################
def get_content_dc(gall_url):
    gall_id = get_gall_id(gall_url)
    url_folder_path = f"./url/{gall_id}"            # 읽어올 폴더 경로 설정
    content_folder_path = f"./content/{gall_id}"    # 저장할 폴더 경로 설정
    util.create_folder(content_folder_path)         # 저장할 폴더 만들기
    error_log = []                                  # 에러 로그 저장 [’error’]
    data_list = []                                  # 데이터 리스트 ['date', 'title', 'url', 'media', 'content', 'is_comment']
    url_csv_file_name = f"url_{gall_id}.csv"        # url csv 파일 이름
    content_file_name = f"content_{gall_id}"        # content 파일 이름

    # 1) url.csv를 df로 읽어옴
    df_url = util.read_file(url_folder_path, url_csv_file_name)

    # 게시글 하나씩 읽어옴 url_row = ['date', 'title', 'url', 'media']
    for index, url_row in df_url.iterrows():
        # 2-a) df_url에서 한 url_row 읽어옴
        # 3-a) 다 끝났으면 다음 url_row 읽어옴
        # 3-b) 2,3 반복
        print(f"[index : {index}] {url_row['url']}")

        # {step 1} 본문 정보 row를 data_list에 추가
        try:
            print("{step 1} 본문 정보를 추가하겠습니다")
            print("1초 기다리기")
            new_row = get_new_row_from_main_content(1, url_row)  # new_row에 정보를 채워둔다
            data_list.append(new_row)   # data_list에 new_row를 추가한다
            print(f"[본문을 추가했습니다] {new_row}")
        except Exception as e:
            # 오류뜨는 것들에 한해, 시간을 넉넉하게 줘서 오류를 방지하고 데이터의 무결성을 유지한다
            print("1초가 너무 짧아서, 10초 기다리겠습니다")
            try:
                new_row = get_new_row_from_main_content(10, url_row)  # new_row에 정보를 채워둔다
                data_list.append(new_row)  # data_list에 new_row를 추가한다
                print(f"[본문을 추가했습니다] {new_row}")
            except Exception as e:
                status = "[{step 1} 본문 정보 row를 data_list에 추가]"
                print(f'[ERROR][index : {index}]{status}[error message : {e}]')
                error_log.append([index, status, e, url_row['title'], url_row['url']])

        # {step 2} 댓글들 정보들을 불러오겠습니다
        # new_row 형식 : ['date', 'title', 'url', 'media', 'content', 'is_comment']
        try:
            print("{step 2} 댓글들 정보들을 불러오겠습니다")
            reply_list = get_reply_list(1, url_row['url'])  # 댓글 리스트 soup
        except Exception as e:
            status = "[댓글들 정보 추가 : driver 불러오기]"
            print(f'[ERROR][index : {index}]{status}[error message : {e}]')
            error_log.append([index, status, e, url_row['title'], url_row['url']])
            continue

        # 댓글이 없으면 다음 글로 넘어감
        if not reply_list:
            print("{step 3} 댓글이 없습니다. 다음 url_row로 넘어갑니다")
            continue
        # 댓글이 있으면 댓글 정보를 가져온다
        for reply in reply_list:
            print("{step 3} 댓글이 존재합니다. 댓글 정보를 크롤링 하겠습니다")
            try:
                # 필요없는 항목 넘어가기
                if is_ignore_reply(reply):
                    continue
                # 댓글 정보 가져오기 : date, content
                date = get_reply_date(reply)
                content = reply.find("p", {"class": "usertxt ub-word"}).text  # 댓글 내용 추출
                content = util.preprocess_content_dc(content)    # 전처리
                new_row = [date, url_row['title'], url_row['url'], url_row['media'], content, 1]  # new_row에 정보를 채워둔다
                data_list.append(new_row)                        # data_list에 new_row를 추가한다
                print(f"[댓글을 추가했습니다] {new_row}")
            except Exception as e:
                status = "[{step 3} 댓글 정보를 크롤링]"
                print(f'[ERROR][index : {index}]{status}[error message : {e}]')
                error_log.append([index, status, e, url_row['title'], url_row['url']])
                continue

    # 4) 끝나면 파일로 저장, 에러 로그 체크
    # 4-a) 결과 csv 파일로 저장
    try:
        df_result = pd.DataFrame(data_list, columns=['date', 'title', 'url', 'media', 'content', 'is_comment'])
        util.save_file(df_result, content_folder_path, f"{content_file_name}.csv")
    except Exception as e:
        print('[error][결과 csv 파일로 저장] ', e)

    # 4-b) 에러 로그 체크, 저장
    try:
        util.error_check(error_log, content_folder_path, content_file_name)
    except Exception as e:
        print('[error][에러 로그 체크] ', e)


##############################################
