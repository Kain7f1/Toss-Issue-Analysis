from dcinside_url_crawler import get_url_dcinside
from dcinside_content_crawler import get_content_dc
import utility_module as util

# 설정값
keyword = "토스"
blacklist = ["토스트", "도리토스", "치토스", "멘토스", "셀토스", "키보토스", "프로토스", "테스토스테론"]
gall_url = {
    "해외주식": "https://gall.dcinside.com/mgallery/board/lists/?id=tenbagger",
    "편의점": "https://gall.dcinside.com/board/lists/?id=cs_new1",
    "신용카드": "https://gall.dcinside.com/board/lists/?id=creditcard",
    "코스피": "https://gall.dcinside.com/mgallery/board/lists?id=kospi",
    "알뜰폰": "https://gall.dcinside.com/mgallery/board/lists?id=mvnogallery",
    "미국주식": "https://gall.dcinside.com/mgallery/board/lists?id=stockus",
    "체크카드": "https://gall.dcinside.com/mgallery/board/lists?id=checkcard",
    "SFF": "https://gall.dcinside.com/mgallery/board/lists?id=sff",
    "토스": "https://gall.dcinside.com/mgallery/board/lists/?id=toss"
}

# 해외주식, 코스피, 체크카드, SFF, 토스
# [1. url 크롤링]
# get_url_dcinside(gall_url["토스"], keyword)

# get_url_dc_toss(keyword, gall_url["토스"])

# [2. content 크롤링]
get_content_dc(gall_url["SFF"])

#########################################
# url = "https://gall.dcinside.com/board/lists/?id=skwyverns_new1&s_type=search_subject_memo&s_keyword=.E3.85.87.E3.85.87"
# a = get_max_page(url)
# print(a)
#########################################
