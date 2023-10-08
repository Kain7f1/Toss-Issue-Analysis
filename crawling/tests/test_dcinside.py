#########################
# 2023-10-08 Hansol Lee
# [실행하기 전에, Users 폴더에 chromedriver.exe를 현재 크롬 버전에 맞게 다운받아주세요]
# 기능 : dcinside 크롤링 실행 함수
#########################

from dcinside_crawler import get_url_dc, get_content_dc

# 설정값
keyword = "에코프로"
gall_name = "해외주식"
# blacklist = ["토스트", "도리토스", "치토스", "멘토스", "셀토스", "키보토스", "프로토스", "테스토스테론"]
gall_url = {
    "미국주식": "https://gall.dcinside.com/mgallery/board/lists?id=stockus",
    "해외주식": "https://gall.dcinside.com/mgallery/board/lists/?id=tenbagger",
    "나스닥": "https://gall.dcinside.com/mgallery/board/lists?id=nasdaq",
    "코스피": "https://gall.dcinside.com/mgallery/board/lists?id=kospi",
    "편의점": "https://gall.dcinside.com/board/lists/?id=cs_new1",
    "신용카드": "https://gall.dcinside.com/board/lists/?id=creditcard",
    "체크카드": "https://gall.dcinside.com/mgallery/board/lists?id=checkcard",
    "알뜰폰": "https://gall.dcinside.com/mgallery/board/lists?id=mvnogallery",
    "SFF": "https://gall.dcinside.com/mgallery/board/lists?id=sff",
    "토스": "https://gall.dcinside.com/mgallery/board/lists/?id=toss"
}


# [1. url 크롤링]
# get_url_dc(gall_url[gall_name], keyword)

# [2. content 크롤링]
get_content_dc(gall_url[gall_name], keyword)
