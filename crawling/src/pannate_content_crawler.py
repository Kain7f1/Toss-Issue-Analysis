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


df_header = pd.DataFrame(columns=['date', 'title', 'url', 'media', 'contents', 'is_comment'])
df_header.to_csv('testing.csv', index=False, encoding='utf-8')
def extract_components_from_urls(url_list):
    try:
        for url in url_list:
            response = requests.get(url)
            time.sleep(2)

            if response.status_code != 200:
                print(f"Failed to get {url}")
                continue

            soup = BeautifulSoup(response.text, 'html.parser')

            #본문  ['date', 'title', 'url', 'media', 'contents', 'is_comment']

            # date 갖고오기
            target_div_date = soup.find('div', {'class': 'info'})
            if target_div_date:
                date_tag = target_div_date.find('span', {'class': 'date'})
                if date_tag:
                    print(f"The text inside the date span from {url} is: {date_tag.text[:10].replace('.', '-')}")
                    final_date = date_tag.text[:10].replace('.', '-')


                else:
                    pass
            else:
                pass

            # title 갖고오기
            target_div = soup.find('div', {'class': 'post-tit-info'})

            if target_div:
                h1_tag = target_div.find('h1')
                if h1_tag:
                    print(f"The text inside the h1 tag from {url} is: {h1_tag.text}")
                    final_title = h1_tag.text.strip()

                else:
                    pass
            else:
                pass

            #Url, media
            final_url = f"{url}"
            final_media = "pannate_teen"

            # content 갖고오기
            target_div_content = soup.find('div', {'id': 'contentArea'})
            if target_div_content:
                print(f"The text inside the content from {url} is: {target_div_content.text.strip()}")
                final_content = target_div_content.text.strip()
                print("content:",final_content)

                # is_comment에 추가
                # 본문:0, 댓글:1
                is_comment_main_text="0"
                print(is_comment_main_text)

            else:
                pass




            #####################################################


            # 댓글 갖고오기
            # 댓글의 date 가져오기
            dt_tags = soup.find_all('dt')


            for dt in dt_tags:
                i_tag = dt.find('i')
                if i_tag:
                    print("Found i tag inside dt:", i_tag)
                    print(i_tag.text[:10].replace('.', '-'))
                    final_date = i_tag.text[:10].replace('.', '-')



            #댓글 컨텐츠
            pattern = re.compile('content_area_\d{8}')
            # 정규식표현으로 댓글태그 형식 지정
            # Note: 네이트판과 같은경우 댓글 태그는 contentArea뒤에 랜덤으로 8자리 숫자가 붙는다
            target_div_reply = soup.find('dd', {'id': pattern})

            if target_div_reply:
                print(target_div_content.text)
                final_content = (target_div_reply.text.strip())
                final_media ="pannate_teen"
                is_comment_main_text = "1"
                print(final_content)
                print(is_comment_main_text)

                #댓글 컨텐츠가 있을 경우 원문 title 텍스트에 대한 내용과 url을 넣어준다
                if target_div:
                    h1_tag = target_div.find('h1')
                    if h1_tag:
                        print(f"The text inside the h1 tag from {url} is: {h1_tag.text}")
                        final_title=h1_tag.text
                        final_url=f"{url}"
                    else:
                        title_lst.append(None)
                else:
                    title_lst.append(None)
            else:
                print("해당하는 div태그가 없습니다")



        new_row.loc[1] = [final_date, final_title, final_url, final_media, final_content, is_comment_main_text]
        new_row.to_csv('testing.csv', mode='a', header=False, index=False, encoding='utf-8')
        return


    except Exception as e:
        print('Error Occurs!', e)


# CSV 파일에서 url 읽어오기
df = pd.read_csv('mock_pannate_teen_url.csv')
urls = df['url'].tolist()

extract_components_from_urls(urls)

