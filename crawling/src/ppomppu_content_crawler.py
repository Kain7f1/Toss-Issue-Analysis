# Library
# Crawling

from bs4 import BeautifulSoup
import requests

# time
import datetime
from datetime import datetime
import time
from calendar import monthrange

# pandas
import pandas as pd
import re


def extract_components_from_urls(url_list):
    data_list = []

    try:
        for url in url_list:
            date = ''
            title = ''
            content = ''
            is_comment_main_text = ''
            media = 'ppomppu_freeboard'

            response = requests.get(url)
            time.sleep(1)
            if response.status_code != 200:
                print(f"Failed to get {url}")
                continue
            soup = BeautifulSoup(response.text, 'html.parser')

            # date 가져오기
            div_text = soup.find('div', class_='sub-top-text-box').get_text()
            match = re.search(r"등록일: ([\d-]+\s[\d:]+)", div_text)

            if match:
                registration_date = match.group(1)
                print("********************************새로운 본문 내용********************************")
                date = registration_date[:10]
                print("이 글의 작성일 입니다:", date)

                # title 가져오기
            target_font_title = soup.find('font', {'class': 'view_title2'}).text
            title = re.sub(r'\s+\d+$', ' ', target_font_title)
            print(f"다음 링크의 내용입니다:{url}")
            print("글의 제목입니다:", title)

            # content 가져오기
            p_tags = soup.find_all('p')
            filtered_p = [p.text.strip() for p in p_tags if len(p.text.strip()) > 30]
            combined_text = ' '.join(filtered_p)
            is_comment_main_text = '0'
            print('본문이면 0, 댓글이면 1로 라벨링:', is_comment_main_text)


            # 삭제해야 하는 것들

            replacements = ['포럼지원센터', '북마크보기', '북마크등록', '재테크포럼 |          보험포럼', '북마크 등록하기',
                            '기본새 카테고리 추가', '북마크관리', '등록하기', '보내기', '이메일 추천하기',
                            '뽐뿌( https://www.ppomppu.co.kr )에서 발송되어진 메일입니다.',
                            '토스뱅크, 2850억 규모 유상증자, 1년내 최대', '클릭하시면 원본 글과 코멘트를 보실수 있습니다.',
                            '전송중입니다. 잠시만 기다려 주세요.']

            for replacement in replacements:
                combined_text = combined_text.replace(replacement, '')

            combined_text = re.sub(r'https:\/\/.*?\s', '', combined_text)
            combined_text = re.sub(r'={2,}', '', combined_text)
            combined_text = re.sub(r'\s+', ' ', combined_text).strip()

            print("본문 내용:", combined_text)

            # data_list에 추가
            data_list.append([date, title, url, media, combined_text, is_comment_main_text])
            print("데이터의 길이:", len(data_list))
            print("********************************본문내용끝********************************")

            #####################################################

            # 댓글의 날짜 가져오기
            target_reply_dates = soup.find_all('font', class_='eng-day')

            # 댓글의 내용 가져오기
            target_content_replies = soup.find_all('div', {'class': 'over_hide link-point mid-text-area'})

            # 댓글이 있을 때만 처리: 각 댓글의 날짜와 내용을 함께 출력
            if len(target_reply_dates) > 0 and len(target_content_replies) > 0:

                for date1, reply1 in zip(target_reply_dates, target_content_replies):
                    print("[댓글 작성 날짜입니다] :", date1.text.strip())
                    print("[댓글 내용입니다.] :", reply1.text.strip())
                    date = date1.text.strip()
                    content = reply1.text.strip()
                    is_comment_main_text = '1'
                    print('본문이면 0, 댓글이면 1로 라벨링:', is_comment_main_text)

                    # data_list에 추가
                    data_list.append([date, title, url, media, combined_text, is_comment_main_text])
            else:
                print("댓글이 없다구용")

            print("********************************댓글은 여기까징********************************")
            print("데이터의 길이:", len(data_list))

    except Exception as e:
        print('Error Occurs!', e)
        pass

    df_result = pd.DataFrame(data_list, columns=['date', 'title', 'url', 'media', 'content', 'is_comment'])
    # df: 클리앙 url 크롤링한 데이터의 df가 할당됨
    # df_result: 위 코드를 통해 만들어진 df

    df_result.to_csv('test_csv.csv', index=False)


# datafile
df = pd.read_csv('testing_ppomppu.csv')
urls = df['url'].tolist()

extract_components_from_urls(urls)