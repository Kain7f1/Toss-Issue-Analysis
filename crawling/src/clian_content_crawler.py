def extract_components_from_urls(url_list):
    data_list = []
    date = ''
    title = ''
    url = urls
    media = 'clian'
    content = ''
    is_comment_main_text = ''

    try:
        for url in url_list:
            response = requests.get(url)
            time.sleep(1)
            if response.status_code != 200:
                print(f"Failed to get {url}")
                continue
            soup = BeautifulSoup(response.text, 'html.parser')

            # 본문  ['date', 'title', 'url', 'media', 'content', 'is_comment']
            # date 가져오기
            print("********************************새로운 본문 내용********************************")
            post_author_div = soup.find('div', class_='post_author')
            date_time_info = post_author_div.find_all('span')[0].text.strip()
            date = date_time_info[:10]
            date = re.sub(r'[\n\t]', '', date).strip()
            print(date)

            # title 가져오기
            target_div_title = soup.find('h3', {'class': 'post_subject'})
            span_tags = target_div_title.find_all('span')
            # Note: 기타, 잡담 등으로 카테고리가 되어 있는가, 해당 게시물에 댓글이 있느냐 없느냐에 따라 슬라이싱을 달리 적용해야함
            try:
                title = span_tags[-3].text
                print("Note: 글의 제목입니다. :", title)
            except IndexError:
                try:
                    title = span_tags[1].text
                    print("Note: 글의 제목입니다. :", title)

                except IndexError:
                    title = span_tags[0].text
                    print("Note: 글의 제목입니다. :", title)

            # content 가져오기
            target_div_content = soup.find('div', class_='post_article')
            # csv파일에 깔끔하게 넣기 위해서 추가적으로 처리(공백처리)
            # content 내용이 없을 경우
            if target_div_content:
                need_clean_content = target_div_content.text.strip()  # need_clean_content: 공백처리 전의 texts
                if len(need_clean_content) == 0:
                    content = re.sub(r'\s+', ' ', need_clean_content.strip())
                    content = title + " " + content
                else:
                    content = re.sub(r'\s+', ' ', need_clean_content.strip())
                    # 이모티콘 지우기(유니코드)
                    content = re.sub(
                        r'[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F700-\U0001F77F]', '',
                        html.strip())

                print(content)
                is_comment_main_text = "0"
                print("본문이면 0, 댓글이면 1로 라벨링 :", is_comment_main_text)

            # 위의 내용 data_list에 넣어주기
            # 2차원 리스트를 만들어서 나중에 dataframe에 넣어줄 것임
            data_list.append([date, title, url, media, content, is_comment_main_text])
            print("데이터의 길이:", len(data_list))
            print("********************************본문내용끝********************************")

            #####################################################
            # 댓글 가져오기
            # 대댓글도 같이 가져오기 때문에 댓글 가져오기 코드로 일괄하여 처리

            target_div_reply_date = soup.find_all('div', class_='comment_time popover')
            target_div_reply = soup.find_all('div', class_="comment_view")

            for dates_div, reply in zip(target_div_reply_date, target_div_reply):
                # 댓글 날짜 처리
                date = dates_div.text.strip()[:10]
                date = re.sub(r'[\n\t]', '', date).strip()
                if ":" in date:
                    date = "2023-10-06"
                    # datetime.now()로 처리해보려고 했으나 계속적으로 오류 발생: 파이참으로 다시한번 체크 예정
                else:
                    date = "2023-" + date
                print(date)
                print("이 글의 댓글입니다.", url)

                # 댓글 내용 처리
                need_clean_content = ' '.join(reply.stripped_strings)
                pattern = r'@.+?님'
                content = re.sub(pattern, '', need_clean_content)
                # 이모티콘 지우기(유니코드)
                content = re.sub(
                    r'[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F700-\U0001F77F]', '',
                    html.strip())
                print(content.strip())

                is_comment_main_text = "1"
                print("본문이면 0, 댓글이면 1로 라벨링 :", is_comment_main_text)

                # 위의 내용 data_list에 넣어주기
                data_list.append([date, title, url, media, content, is_comment_main_text])

                #
                print("데이터의 길이:", len(data_list))
                print("***********************************댓글내용끝********************************")





    except Exception as e:
        print('Error Occurs!', e)
        return []

    df_result = pd.DataFrame(data_list, columns=['date', 'title', 'url', 'media', 'content', 'is_comment'])
    # df: 클리앙 url 크롤링한 데이터의 df가 할당됨
    # df_result: 위 코드를 통해 만들어진 df

    df_result.to_csv('clian_content.csv', index=False)


# datafile
df = pd.read_csv('clian_url_crawling.csv')
urls = df['url'].tolist()

extract_components_from_urls(urls)