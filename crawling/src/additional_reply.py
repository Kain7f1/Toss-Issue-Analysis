for dt in reply_dt_tags:
    i_tag = dt.find('i')  # 각 dt 태그 내의 첫 번째 i 태그를 찾음
    if i_tag:
        print("대댓글의 날짜:", i_tag)
        final_date = i_tag.text[:10].replace('.', '-')

pattern_surplus_reply = re.compile('content_area_\d{9}')

# 정규식표현으로 대댓글태그 형식 지정
target_div_surplus_reply = soup.find('dd', {'id': pattern_surplus_reply})

if target_div_surplus_reply:
    # date 추출
    span_tags = soup.find_all('span', {'class': 'usertxt'})

    for span in span_tags:
        print("날짜", span.text)

    for dt in dt_tags:
        i_tag = dt.find('i')  # 각 dt 태그 내의 첫 번째 i 태그를 찾음
        if i_tag:
            final_date = i_tag.text[:10].replace('.', '-')
            print("대댓글의 날짜:", final_date)

    final_content = (target_div_reply.text.strip())
    final_media = "pannate_teen"
    is_comment_main_text = "1"
    print(final_content)
    print(is_comment_main_text)

    print(f"The text inside the content from {url} is: {target_div_surplus_reply.text.strip()}")


else:
    print("Error! 대댓글이 없습니다.")