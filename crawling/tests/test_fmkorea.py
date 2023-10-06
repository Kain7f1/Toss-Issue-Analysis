from fmkorea_crawler import get_url_fmkorea, get_content

# 설정값
keyword = "토스"
start_date = "2015-02-26"
end_date = "2023-09-19"

# [url 크롤링]
get_url_fmkorea(keyword, start_date, end_date)

# [content 크롤링]
# media = {"토스갤": "dcinside_toss"}
# get_content(media["토스갤"])
