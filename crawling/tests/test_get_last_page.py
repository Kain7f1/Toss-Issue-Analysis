import crawling_tool as cr

headers_dc = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
        "Connection": "keep-alive",
        "Cache-Control": "max-age=0",
        "sec-ch-ua-mobile": "?0",
        "DNT": "1",
        "Upgrade-Insecure-Requests": "1",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-User": "?1",
        "Sec-Fetch-Dest": "document",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "ko-KR,ko;q=0.9"
    }

url_1 = "https://gall.dcinside.com/mgallery/board/lists/?id=kospi&page=1&search_pos=-2870000&s_type=search_subject_memo&s_keyword=.6C.67.ED.99.94.ED.95.99"
url_2 = "https://gall.dcinside.com/mgallery/board/lists/?id=kospi&s_type=search_subject_memo&s_keyword=.EB.BD.95"
url_15 = "https://gall.dcinside.com/mgallery/board/lists/?id=kospi&page=1&search_pos=-3302751&s_type=search_subject_memo&s_keyword=.EC.94.A8.EB.B0.9C"
url_16 = "https://gall.dcinside.com/mgallery/board/lists/?id=kospi&page=1&search_pos=-3292751&s_type=search_subject_memo&s_keyword=.EC.94.A8.EB.B0.9C"
url_44 = "https://gall.dcinside.com/mgallery/board/lists?id=kospi&s_type=search_subject_memo&s_keyword=.E3.85.87"
soup = cr.get_soup_from_url(url_16)
print("len_soup :", len(soup))
last_page = cr.get_last_page(soup)
print("last_page :", last_page)


#################################
# get_last_page() 예전 버전
#################################
# def get_last_page(url, time_sleep=0):
#     try:
#         with requests.Session() as session:
#             response = session.get(url, headers=headers)
#             time.sleep(time_sleep)
#         soup = BeautifulSoup(response.text, "html.parser")
#         filtered_a_tags = [a for a in soup.find_all('a') if not a.find('span', class_='sp_pagingicon')]
#         num_button_count = len(filtered_a_tags) + 1    # 숫자 버튼의 개수
#         if num_button_count >= 16:    # 한번에 15 page씩 나와서, page가 16개 이상이면 >> 버튼이 생기면서 a태그가 17개가 된다 / 이때의 페이징 처리
#             last_page_url = soup.find_all("a")[-2]['href']                          # 맨 마지막 페이지로 가는 버튼의 url
#             last_page = re.search(r'page=(\d+)', last_page_url).group(1)     # 정규식으로 page 부분의 숫자만 추출
#             last_page = int(last_page)                                              # 맨 마지막 페이지
#         else:
#             last_page = num_button_count
#     except Exception as e:
#         print(f"[오류 발생, 반복] [get_last_page(time_sleep={time_sleep})] ", e)
#         last_page = get_last_page(url, time_sleep+2)
#     return last_page
#
#####################################
