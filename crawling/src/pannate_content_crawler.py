# 라이브러리
import pandas as pd
import requests
from bs4 import BeautifulSoup
import re

import time


# Func info: url에서 url의 component를 뽑아냅니다
# input: csv파일로 만든 url_list를 넣어줍니다
# output: {media}_content_crawling.csv를 만들어줍니다.
# columns: [date, title, url, media, contents, is_comment]




def extract_components_from_urls(url_list):
    data_list = []
    final_date = ''
    final_title = ''
    final_url = ''
    final_media = ''
    final_content = ''
    is_comment_main_text = ''
    try:
        for url in url_list:
            response = requests.get(url)
            time.sleep(1)
            if response.status_code != 200:
                print(f"Failed to get {url}")
                continue
            soup = BeautifulSoup(response.text, 'html.parser')

            # 본문  ['date', 'title', 'url', 'media', 'contents', 'is_comment']
            # date 갖고오기
            target_div_date = soup.find('div', {'class': 'info'})
            if target_div_date:
                date_tag = target_div_date.find('span', {'class': 'date'})
                if date_tag:
                    print(f"{url}의 본문 작성일: {date_tag.text[:10].replace('.', '-')}")
                    final_date = date_tag.text[:10].replace('.', '-')           # 한솔 : 변수 맨처음에 선언해주고 사용해주세요

            # title 갖고오기
            target_div = soup.find('div', {'class': 'post-tit-info'})
            if target_div:
                h1_tag = target_div.find('h1')
                if h1_tag:
                    print(f"{url}의 컨텐츠 내용: {h1_tag.text}")
                    final_title = h1_tag.text.strip()

            # Url, media
            final_url = f"{url}"
            final_media = "pannate_teen"

            # content 갖고오기
            target_div_content = soup.find('div', {'id': 'contentArea'})
            if target_div_content:
                final_content = target_div_content.text.strip()
                print("content:", final_content)
                # is_comment에 추가
                # 본문:0, 댓글:1
                is_comment_main_text = "0"
                print("본문이면 0, 댓글이면 1로 라벨링 :", is_comment_main_text)

            #내용을 data_list에 넣어준다
            data_list.append([final_date, final_title, final_url, final_media, final_content, is_comment_main_text])



            #####################################################

            # 댓글 갖고오기
            # 댓글의 date 가져오기
            dt_tags = soup.find_all('dt')
            for dt in dt_tags:
                i_tag = dt.find('i')
                if i_tag:
                    print(f"{url}에 달린 댓글 작성일:",i_tag.text[:10].replace('.', '-'))
                    final_date = i_tag.text[:10].replace('.', '-')

            # 댓글 컨텐츠
            pattern = re.compile('content_area_\d{8}')
            # 정규식표현으로 댓글태그 형식 지정
            # Note: 네이트판과 같은경우 댓글 태그는 contentArea뒤에 랜덤으로 8자리 숫자가 붙는다
            target_div_replys = soup.find_all('dd', {'id': pattern})

            if target_div_replys:  # 리스트가 비어있지 않을 경우만 실행
                for target_div_reply in target_div_replys:
                    final_content = target_div_reply.text.strip()
                    final_media = "pannate_teen"
                    is_comment_main_text = "1"

                    print(f"{url}에 달린 댓글내용:", final_content.strip().replace('\n', ''))
                    print("본문이면 0, 댓글이면 1로 라벨링 :", is_comment_main_text)

                    if target_div:
                        h1_tag = target_div.find('h1')
                        if h1_tag:
                            final_title = h1_tag.text.strip()
                            final_url = f"{url}"

                    data_list.append(
                        [final_date, final_title, final_url, final_media, final_content, is_comment_main_text])
            else:
                print("이 글에는 댓글이 없습니다")


            # # 대댓글 갖고오기

            # # 대댓글의 날짜 가져오기

            additional_reply_space = soup.find('ul', {'class': 'replelist f_clear'})
            if additional_reply_space:
                dd_tags = additional_reply_space.find_all('dd')

                for dd in dd_tags:
                    print(dd.text)


            # addtional_reply_date = soup.find_all('dt')
            # for dt in addtional_reply_date:
            #     i_tag = dt.find('i')
            #     if i_tag:
            #         print(f"{url}에 달린 대댓글 작성일:", i_tag.text[:10].replace('.', '-'))
            #         final_date = i_tag.text[:10].replace('.', '-')
            #
            # # # 대댓글의 컨텐츠 갖고오기
            # additional_reply_pattern = re.compile('content_area_\d{9}')
            # additional_replies = soup.find_all('dd', {'id': additional_reply_pattern})
            #
            # if additional_replies:  # 리스트가 비어있지 않을 경우만 실행
            #     for addtional_reply in additional_replies:
            #         final_contents = addtional_reply.text.strip()
            #         final_media = "pannate_teen"
            #         is_comment_main_text = "1"
            #
            #         print(f"{url}에 달린 대댓글내용:", final_contents.strip().replace('\n', ''))
            #         print("본문이면 0, 댓글이면 1로 라벨링 :", is_comment_main_text)

                    # if target_div:
                    #     h1_tag = target_div.find('h1')
                    #     if h1_tag:
                    #         final_title = h1_tag.text.strip()
                    #         final_url = f"{url}"
                    #
                    # data_list.append(
                    #     [final_date, final_title, final_url, final_media, final_content, is_comment_main_text])


            print("*"*100)
            print(len(data_list))




        return



    except Exception as e:
        print('Error Occurs!', e)

