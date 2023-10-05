# Made by Hansol Lee 20230925

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


##############################
# get_gall_id()
# 기능 : gall_url을 받아 gall_id를 리턴한다
def get_gall_id(gall_url):
    return re.search(r'id=([\w_]+)', gall_url).group(1)


##############################
# get_gall_type()
# 기능 : 메이저갤러리인지 마이너갤러리인지 미니갤러리인지 판단한다
# 리턴값 : 메이저갤러리('major'), 마이너갤러리('minor'), 미니갤러리('mini')
def get_url_base(gall_url):
    if "mgallery" in gall_url:
        url_base = "https://gall.dcinside.com/mgallery"
    elif "mini" in gall_url:
        url_base = "https://gall.dcinside.com/mini"
    else:
        url_base = "https://gall.dcinside.com"
    return url_base


###############################
# get_max_num()
# 기능 : 검색결과 중 가장 큰 글번호를 구하여 리턴한다
# 리턴값 : max_num
def get_max_num(keyword, gall_id, url_base):
    search_url = f"{url_base}/board/lists/?id={gall_id}&s_type=search_subject_memo&s_keyword={keyword}"
    print(search_url)
    response = requests.get(search_url, headers=header)
    soup = BeautifulSoup(response.text, "html.parser")  # 페이지의 soup
    box = soup.select("div.gall_listwrap tr.ub-content")        # 글만 있는 box
    first_content = ''
    # 검색 범위를 정하는 작업
    for content in box:
        # 광고는 제거한다 : 광고글은 글쓴이가 "운영자"이다
        if content.find('td', class_='gall_writer').get_text() == "운영자":
            continue
        # 광고를 제외한 가장 첫번째 글
        first_content = content.select_one("td.gall_num").get_text()
        break
    max_num = int(int(first_content)/10000+1)*10000      # max_num  의 글번호까지 검색한다
    return max_num


################################
# get_max_page()
# 기능 : [dcinside] 갤러리 내에서 검색결과의 마지막 페이지가 몇인지 리턴 (검색한 직후의 url이어야 함)
# 리턴값 : max_page(int)
def get_last_page(url):
    response = requests.get(url, headers=header)
    soup = BeautifulSoup(response.text, "html.parser").find("div", class_="bottom_paging_wrap re")
    filtered_a_tags = [a for a in soup.find_all('a') if not a.find('span', class_='sp_pagingicon')]
    num_button_count =  len(filtered_a_tags) + 1    # 숫자 버튼의 개수

    if num_button_count >= 16:    # 한번에 15 page씩 나와서, page가 16개 이상이면 >> 버튼이 생기면서 a태그가 17개가 된다 / 이때의 페이징 처리
        last_page_url = soup.find_all("a")[-2]['href']                          # 맨 마지막 페이지로 가는 버튼의 url
        last_page = re.search(r'page=(\d+)', last_page_url).group(1)     # 정규식으로 page 부분의 숫자만 추출
        last_page = int(last_page)                                              # 맨 마지막 페이지
    else:
        last_page = num_button_count

    return last_page


################################
# 목적 : 글 url 받아오기 - 토스 갤러리
# 입력값 : 입력 키워드(토스), 시작 날짜(20150226), 종료 날짜(20230919)
# 리턴 : x
# 생성 파일 : url_dcinside_toss.csv
# columns = ['date', 'title', 'url', 'media']
def get_url_dc_toss(keyword):
    media = "dcinside_toss"  # 토스 갤러리 media column
    header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"}
    folder_path = f"./url/{media}"  # 저장할 폴더 경로 설정
    util.create_folder(folder_path)      # 폴더 만들기
    error_log = []                  # 에러 로그 저장 [’error’]
    data_list = []                  # 데이터 리스트 ['date', 'title', 'url', 'media']
    file_name = f"url_{media}"      # 저장할 파일 이름
    count_pinned_post = 3           # 고정상단글, 공지 같은거 개수
    first_index = "-1"              # 고정상단글 제외한 첫번째 글의 글인덱스/ 이걸로 마지막 페이지인지 체크함
    is_end = False                  # 모든 크롤링 완료했으면 True

    # 1. 크롤링
    for page in range(1, 10000):
        try:
            search_url = f"https://gall.dcinside.com/mgallery/board/lists/?id=toss&page={page}"
            response = requests.get(search_url, headers=header)
            soup = BeautifulSoup(response.text, "html.parser")  # 페이지의 soup
            soup_box = soup.select("article")[1]                        # 50개 게시글 있는 박스 soup
            element_list = soup_box.select("tbody tr")[count_pinned_post:]  # 한 페이지 전체 글 리스트, 고정상단글 제외
            for index, element in enumerate(element_list):
                td_list = element.select("td")                      # element의 요소들 리스트
                # first_index 와 비교하여 마지막 페이지인지 판단함
                temp_first_index = td_list[0].get_text(strip=True)
                if index == 0:
                    if first_index == temp_first_index:
                        print("first_index : ", first_index)
                        print("temp_first_index : ", temp_first_index)
                        print("마지막 페이지이므로 종료합니다")
                        is_end = True       # 종료
                        break
                    else:
                        first_index = temp_first_index  # 마지막 페이지가 아니면 first_index를 업데이트함
                # new_row 에 정보 입력
                date = td_list[4]['title'][:10]
                title = util.preprocess_title(td_list[2].get_text(strip=True))
                url = "https://gall.dcinside.com" + td_list[2].find('a')['href']
                new_row = [date, title, url, media]
                data_list.append(new_row)   # data_list에 크롤링한 정보 저장
                print(f"[page : {page}] new_row : {new_row}")
            if is_end:
                break
        except Exception as e:
            print('[error occured] ', e)
            error_log.append([e])
            break

    # 2. 파일저장
    try:
        df_result = pd.DataFrame(data_list, columns=['date', 'title', 'url', 'media'])
        util.save_file(df_result, folder_path, f"{file_name}.csv")
    except Exception as e:
        print('[error occured] ', e)
        error_log.append([e])

    # 3. 에러로그확인
    try:
        util.error_check(error_log, folder_path, file_name)
    except Exception as e:
        print('[error occured] ', e)




