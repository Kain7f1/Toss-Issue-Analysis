# Made by Hansol Lee 20230927

import utility_module as utility
from bs4 import BeautifulSoup
import requests
import json
# ----------------------
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

# -----------------------
# 목적 : url.csv를 읽어오고, 각 페이지의 정보를 추출하여 저장한다
# 입력값 : media
# 리턴 : x
# 생성 파일 : content_dcinside_toss.csv
# columns = ['date', 'title', 'url', 'media', 'content', 'is_comment']


def get_content(media):
    # media = "dcinside_toss"  # 토스 갤러리 media column
    header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"}
    url_folder_path = f"./url/{media}"          # 읽어올 폴더 경로 설정
    content_folder_path = f"./content/{media}"  # 저장할 폴더 경로 설정
    utility.create_folder(content_folder_path)  # 저장할 폴더 만들기
    error_log = []                  # 에러 로그 저장 [’error’]
    data_list = []                  # 데이터 리스트 ['date', 'title', 'url', 'media', 'content', 'is_comment']
    url_csv_file_name = f"url_{media}.csv"      # 저장할 파일 이름
    is_end = False                  # 모든 크롤링 완료했으면 True

    # 1) url.csv를 df로 읽어옴
    # 2-a) df에서 한 row 읽어옴
    # 2-b) 본문 정보 row를 data_list에 추가
    # 2-c) 댓글들 정보 row를 data_list에 추가
    # 3) 다 끝났으면 다음 row 읽어옴
    # 2,3 반복
    # 4) 끝나면 파일로 저장, 에러로그 체크

    # data_list에 한 row씩 추가함 : ['date', 'title', 'url', 'media', 'content', 'is_comment']
    # 본문은 content = title + " " + content
    df_url = utility.read_file(url_folder_path, url_csv_file_name)  # url 파일에서 정보 읽어오기
    for index, row in df_url.iterrows():        # 한 줄 씩 읽어옴 ['date', 'title', 'url', 'media']
        try:
            # 2-a) df에서 한 row 읽어옴
            url = row['url']
            print(url)

            driver = get_driver(url)

            response = requests.get(url, headers=header)

            soup = BeautifulSoup(response.text, "html.parser")  # 페이지의 soup
            # ----------------------------------------------------------------------------------------
            # print(soup)

            # data = json.loads(response.text)
            # print(data)

            result = driver.find_elements_by_class_name("ub-content")
            print(type(result))




            # 2-b) 본문 정보 row를 data_list에 추가



            # 2-c) 댓글들 정보 row를 data_list에 추가


        except Exception as e:
            print(f'[error occured] [index : {index}] [error message : {e}]')
            error_log.append([e])
            continue

# ---------------------------

def get_driver(url):
    options = webdriver.ChromeOptions()
    options.add_argument('headless')  # 창이 없이 크롬이 실행이 되도록 만든다
    # options.add_argument("--start-maximized")  # 창이 최대화 되도록 열리게 한다.
    options.add_argument("disable-infobars")  # 안내바가 없이 열리게 한다.
    options.add_argument('--disable-dev-shm-usage')  # 공유메모리를 사용하지 않는다
    options.add_argument("disable-gpu")  # 크롤링 실행시 GPU를 사용하지 않게 한다.
    options.add_argument("--disable-extensions")  # 확장팩을 사용하지 않는다.
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    # site에 접근하기 위해 get메소드에 이동할 URL을 입력한다.
    driver.get(url)
    return driver

    # for page in range(1, 10000):
    #     try:
    #         search_url = f"https://gall.dcinside.com/mgallery/board/lists/?id=toss&page={page}"
    #         response = requests.get(search_url, headers=header)
    #         soup = BeautifulSoup(response.text, "html.parser")  # 페이지의 soup
    #         soup_box = soup.select("article")[1]                        # 50개 게시글 있는 박스 soup
    #         element_list = soup_box.select("tbody tr")[count_pinned_post:]  # 한 페이지 전체 글 리스트, 고정상단글 제외
    #         for index, element in enumerate(element_list):
    #             td_list = element.select("td")                      # element의 요소들 리스트
    #             temp_first_index = td_list[0].get_text(strip=True)  # first_index 와 비교하여 마지막 페이지인지 판단함
    #             if index == 0:
    #                 if first_index == temp_first_index:
    #                     print("first_index : ", first_index)
    #                     print("temp_first_index : ", temp_first_index)
    #                     print("마지막 페이지이므로 종료합니다")
    #                     is_end = True       # 종료
    #                     break
    #                 else:
    #                     first_index = temp_first_index
    #             date = td_list[4]['title'][:10]
    #             title = utility.preprocess_title(td_list[2].get_text(strip=True))
    #             url = "gall.dcinside.com" + td_list[2].find('a')['href']
    #             new_row = [date, title, url, media]
    #             data_list.append(new_row)
    #             print(f"[page : {page}] new_row : {new_row}")
    #         if is_end:
    #             break
    #     except Exception as e:
    #         print('[error occured] ', e)
    #         error_log.append([e])
    #         break
    #
    # # 2. 파일저장
    # try:
    #     df_result = pd.DataFrame(data_list, columns=['date', 'title', 'url', 'media', 'content', 'is_comment'])
    #     utility.save_file(df_result, content_folder_path, f"{file_name}.csv")
    # except Exception as e:
    #     print('[error occured] ', e)
    #
    # # 3. 에러로그확인
    # try:
    #     utility.error_check(error_log, content_folder_path, file_name)
    # except Exception as e:
    #     print('[error occured] ', e)















