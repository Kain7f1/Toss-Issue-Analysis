from dcinside_content_crawler import get_content_dc
from dcinside_url_crawler import get_url_dc_toss

# 설정값
# keyword = "토스"
# start_date = "2015-02-26"
# end_date = "2023-09-19"

# [1. url 크롤링]
# get_url_dc_toss(keyword, start_date, end_date)

# [2. content 크롤링]
media = {"토스갤": "dcinside_toss"}
get_content_dc(media["토스갤"])
