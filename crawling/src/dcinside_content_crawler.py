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
# get_content()
# 목적 : url.csv를 읽어오고, 각 페이지의 정보를 추출하여 저장한다
# 입력값 : media
# 리턴값 : 없음
# 생성 파일 : content_dcinside_toss.csv
# columns = ['date', 'title', 'url', 'media', 'content', 'is_comment']
def get_content_dc(gall_url):
    gall_id = get_gall_id(gall_url)
    url_folder_path = f"./url/{gall_id}"              # 읽어올 폴더 경로 설정
    content_folder_path = f"./content/{gall_id}"      # 저장할 폴더 경로 설정
    util.create_folder(content_folder_path)      # 저장할 폴더 만들기
    error_log = []                                  # 에러 로그 저장 [’error’]
    data_list = []                                  # 데이터 리스트 ['date', 'title', 'url', 'media', 'content', 'is_comment']
    url_csv_file_name = f"url_{gall_id}.csv"          # url 파일 이름
    content_csv_file_name = f"content_{gall_id}.csv"  # content 파일 이름
    now_year = str(datetime.datetime.now().year)    # 올해 년도

    #################################
    # 1) url.csv를 df로 읽어옴
    # 2-a) df에서 한 row 읽어옴
    # 2-b) 본문 정보 row를 data_list에 추가
    # 2-c) 댓글들 정보 row를 data_list에 추가
    # 3-a) 다 끝났으면 다음 row 읽어옴
    # 3-b) 2,3 반복
    # 4) 끝나면 파일로 저장, 에러로그 체크
    #################################
    # 1) url.csv를 df로 읽어옴
    df_url = util.read_file(url_folder_path, url_csv_file_name)
    # 게시글 하나씩 읽어옴 ['date', 'title', 'url', 'media']
    for index, row in df_url.iterrows():
        # row는 ['date', 'title', 'url', 'media'] 형태
        # 2-a) df에서 한 row 읽어옴
        # 3-a) 다 끝났으면 다음 row 읽어옴
        # 3-b) 2,3 반복
        title = row['title']    # 게시글 제목
        url = row['url']        # 게시글 url
        media = row['media']    # 게시글 media
        print(f'[index : {index}] {url}')

        # 2-b) 본문 정보 row를 data_list에 추가
        try:
            response = requests.get(url, headers=header)
            time.sleep(2)
            soup = BeautifulSoup(response.text, "html.parser")
            content = util.preprocess_content_dc(soup.find('div', {"class": "write_div"}).text)  # 전처리
            content = title + " " + content      # 본문이 짧을 때는 제목에 메세지가 담겨있는 경우가 많아서 이렇게 처리함
            new_row = [row['date'], title, url, media, content, 0]  # new_row에 정보를 채워둔다
            data_list.append(new_row)   # data_list에 new_row를 추가한다
            print(new_row)
        except Exception as e:
            step = "[본문 정보 row를 data_list에 추가]"
            print(f'[error][index : {index}]{step}[error message : {e}]')
            error_log.append([index, url, step, e])

        # 2-c) 댓글들 정보 row들을 data_list에 추가
        # new_row 형식 : ['date', 'title', 'url', 'media', 'content', 'is_comment']
        try:
            # 댓글 전부 가져오기
            driver = get_driver()
            driver.get(url)
            time.sleep(1)
            soup = BeautifulSoup(driver.page_source, "html.parser")
            reply_list = soup.find_all("li", {"class": "ub-content"})   # 댓글 리스트 soup
        except Exception as e:
            step = "[댓글들 정보 추가 : driver 불러오기]"
            print(f'[error][index : {index}]{step}[error message : {e}]')
            error_log.append([index, url, step, e])
            continue

        # 댓글이 없으면 다음 글로 넘어감
        if not reply_list:
            print("댓글이 없습니다")
            continue
        # 댓글이 있으면 댓글 정보를 가져온다
        for reply in reply_list:
            try:
                # 필요없는 항목 넘어가기
                if reply.select_one("p.del_reply"):
                    print("[삭제된 코멘트입니다]")
                    continue
                if reply.find('span', {'data-nick': '댓글돌이'}):
                    print("[댓글돌이는 무시합니다]")
                    continue
                if reply.find('div', {'class': 'comment_dccon'}):
                    print("[디시콘은 무시합니다]")
                    continue
                # 댓글 정보 가져오기 : date, content
                date = reply.find("span", {"class": "date_time"}).text.replace(".", "-")  # 댓글 등록 날짜 추출
                if date[:2] == "20":    # 작년 이전은 "2022.09.07 10:10:54" 형식임
                    date = date[:10]
                else:                   # 올해는 "09.30 10:10:54" 형식임
                    date = now_year + "-" + date[:5]
                content = reply.find("p", {"class": "usertxt ub-word"}).text  # 댓글 내용 추출
                content = util.preprocess_content_dc(content)    # 전처리
                new_row = [date, title, url, media, content, 1]  # new_row에 정보를 채워둔다
                data_list.append(new_row)                        # data_list에 new_row를 추가한다
                print(new_row)
            except Exception as e:
                step = "[댓글들 정보 가져와서 data_list에 추가]"
                print(f'[error][index : {index}]{step}[error message : {e}]')
                error_log.append([index, url, step, e])
                continue

    # 4) 끝나면 파일로 저장, 에러 로그 체크
    # 4-a) 결과 csv 파일로 저장
    try:
        df_result = pd.DataFrame(data_list, columns=['date', 'title', 'url', 'media', 'content', 'is_comment'])
        util.save_file(df_result, content_folder_path, f"{content_csv_file_name}.csv")
    except Exception as e:
        print('[error][결과 csv 파일로 저장] ', e)

    # 4-b) 에러 로그 체크
    try:
        util.error_check(error_log, content_folder_path, content_csv_file_name)
    except Exception as e:
        print('[error][에러 로그 체크] ', e)


##############################################
