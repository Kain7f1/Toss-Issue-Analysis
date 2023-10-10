#############################
# Made by Hansol Lee
# 20230927
#############################
import crawling_tool as cr
import utility_module as util
import pandas as pd


##############################################
# 목적 : 디시인사이드 글 url 받아오기
# 입력값 : 입력 키워드(토스), 갤러리 id
# 리턴 : x
# 생성 파일 : url_dcinside_{gall_id}.csv
# columns = ['date', 'title', 'url', 'media']
@util.timer_decorator
def get_url_dc(gall_url, keyword, blacklist):
    # 0. 기본값 세팅 단계
    try:
        keyword_unicode = util.convert_to_unicode(keyword)   # 입력받은 키워드를 유니코드로 변환한다
        gall_id = cr.get_gall_id(gall_url)                   # 갤러리 id
        print("gall_id : ", gall_id)
        url_base = cr.get_url_base(gall_url)  # "https" 부터 "board/" 이전까지의 url 부분 (major갤, minor갤, mini갤)
        print("url_base : ", url_base)
        max_num = cr.get_max_num(gall_url, gall_id)   # 검색결과 중, 가장 큰 글번호 10000단위로 올림한 값/10000
        print("max_num : ", max_num)
        folder_path = f"./url/{keyword}"        # 저장할 폴더 경로 설정
        util.create_folder(folder_path)         # 폴더 만들기
        error_log = []                          # 에러 로그 저장
        data_list = []                          # 데이터 리스트 ['date', 'title', 'url', 'media']
        file_name = f"url_{keyword}_{gall_id}"            # 저장할 파일 이름
        url = '_'
    except Exception as e:
        print("[기본값 세팅 단계에서 error가 발생함] ", e)
        print("[get_url_dcinside() 종료]")
        return 0

    # 1. url 크롤링
    for search_pos in range(max_num, 0, -10000):
        print(f"[1만 개 단위로 검색합니다. 검색어 : {keyword}] " + "*"*100)
        print(f"[search_pos : {search_pos}] " + "*"*100)
        temp_url = f"{url_base}/board/lists/?id={gall_id}&page=1&search_pos=-{search_pos}&s_type=search_subject_memo&s_keyword={keyword_unicode}"
        last_page = cr.get_last_page(temp_url)     # 1만 단위 검색결과의 마지막 페이지
        # 해외주식갤러리처럼 컨텐츠 많을때, 1,2,3,4,5 이렇게 페이징 되어있는거 있음. 이걸 페이지 넘기면서 크롤링
        for page in range(1, last_page+1):
            # [검색결과 페이지 불러오기]
            print(f"[크롤링 남은 글 갯수 : {search_pos}][page : {page}/{last_page}]")
            search_url = f"{url_base}/board/lists/?id={gall_id}&page={page}&search_pos=-{search_pos}&s_type=search_subject_memo&s_keyword={keyword_unicode}"
            element_list = cr.get_search_result(search_url)
            print(f"[글 개수 : {len(element_list)}]")
            # 글 하나씩 뽑아서 크롤링
            for element in element_list:    # element는 글 하나
                # [검색결과에서 글 하나씩 크롤링]
                is_contine, new_row = cr.get_new_row_from_search_result(element, gall_id, blacklist)
                if is_contine:  # 광고글이거나, 제목에 블랙리스트에 있는 단어가 있으면
                    continue    # 다음 element로 넘어간다
                else:                           # 정상적이면
                    data_list.append(new_row)   # data_list에 크롤링한 정보 저장
                print(f"[page {page}/{last_page}] new_row : {new_row}")

    # 2. 파일로 저장
    try:
        print(f"[저장된 url 정보 개수] {len(data_list)}개")
        print(f"[갤러리 주소] {gall_url}")
        df_result = pd.DataFrame(data_list, columns=['date', 'title', 'url', 'media'])
        util.save_file(df_result, folder_path, f"{file_name}.csv")
    except Exception as e:
        status = "[파일 저장할 때 오류 발생]"
        print('[error] ', e)
        error_log.append([url, status, e])

    # 3. 에러로그확인
    try:
        util.error_check(error_log, folder_path, file_name)
    except Exception as e:
        print('[error로그 추가할 때 오류 발생] ', e)


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
@util.timer_decorator
def get_content_dc(gall_url, keyword, blacklist):
    gall_id = cr.get_gall_id(gall_url)
    url_folder_path = f"./url/{keyword}"            # 읽어올 폴더 경로 설정
    content_folder_path = f"./content/{keyword}"    # 저장할 폴더 경로 설정
    util.create_folder(content_folder_path)         # 저장할 폴더 만들기
    error_log = []                                  # 에러 로그 저장 [’error’]
    data_list = []                                  # 데이터 리스트 ['date', 'title', 'url', 'media', 'content', 'is_comment']
    url_file_name = f"url_{keyword}_{gall_id}"        # url csv 파일 이름
    content_file_name = f"content_{keyword}_{gall_id}"        # content 파일 이름

    # 1) url.csv를 df로 읽어옴
    df_url = util.read_file(url_folder_path, f"{url_file_name}.csv")
    len_df = len(df_url)
    # 게시글 하나씩 읽어옴 url_row = ['date', 'title', 'url', 'media']
    for index, url_row in df_url.iterrows():
        # 2-a) df_url에서 한 url_row 읽어옴
        # 3-a) 다 끝났으면 다음 url_row 읽어옴
        # 3-b) 2,3 반복
        title = url_row['title']
        url = url_row['url']
        print(f"[{index+1}/{len_df}] 본문 페이지 : {url}")
        if cr.is_deleted_page(url):     # 글이 삭제되었는지 검사
            continue    # 글이 삭제되었으면, 다음 row로 넘어갑니다
        # {step 1} 본문 정보 row를 data_list에 추가
        print("{step 1 시작} 본문 정보를 추가하겠습니다")
        new_row = cr.get_new_row_from_main_content(url_row)  # ['date','title','url','media','content','is_comment']
        if util.contains_blacklist(new_row[-2], blacklist):
            print("{step 1~3 종료} content에 blacklist에 해당하는 단어 발견 : ", new_row[-2])
            continue    # 블랙리스트에 해당하는 내용이 있으면, 다음 row로 넘어갑니다
        else:
            data_list.append(new_row)                                         # data_list에 new_row를 추가한다
            print("{step 1 종료} 본문을 추가했습니다", new_row[0], new_row[-2])

        # {step 2} 댓글들 정보들을 불러오겠습니다
        # new_row 형식 : ['date', 'title', 'url', 'media', 'content', 'is_comment']
        print("{step 2 시작} 댓글 정보들을 불러오겠습니다")
        reply_list = cr.get_reply_list(url)  # 댓글 리스트 soup
        print("{step 2 종료} 댓글 정보들을 불러왔습니다")

        # 댓글이 없으면 다음 글로 넘어감
        if not reply_list:
            print("{step 3 종료} 댓글이 없습니다. 다음 url_row로 넘어갑니다")
            continue
        # 댓글이 있으면 댓글 정보를 가져온다
        print("{step 3 시작} 댓글이 존재합니다. 댓글 정보를 크롤링 하겠습니다")
        for reply in reply_list:
            try:
                # 필요없는 항목 넘어가기
                if cr.is_ignore_reply(reply):
                    continue
                # 댓글 정보 가져오기 : date, content
                date = cr.get_reply_date(reply)
                content = reply.find("p", {"class": "usertxt ub-word"}).text  # 댓글 내용 추출
                content = util.preprocess_content_dc(content)    # 전처리
                new_row = [date, title, url, gall_id, content, 1]  # new_row에 정보를 채워둔다
                data_list.append(new_row)                        # data_list에 new_row를 추가한다
                print(f"[댓글을 추가했습니다] {new_row}")
            except Exception as e:
                status = "[{step 3} 댓글 정보를 크롤링]"
                print(f'[ERROR][index : {index}]{status}[error message : {e}]')
                error_log.append([index, status, e, title, url])
                continue
        print("{step 3 종료} 댓글 크롤링을 종료합니다")
    # 4) 끝나면 파일로 저장, 에러 로그 체크
    # 4-a) 결과 csv 파일로 저장
    try:
        print(f"[{len(data_list)}개의 content 정보가 저장되었습니다]")
        print(f"[갤러리 주소 : {gall_url}]")
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
