#############################################################################
# 2023-10-08 Hansol Lee
# [실행하기 전에, Users 폴더에 chromedriver.exe를 현재 크롬 버전에 맞게 다운받아주세요]
# 기능 : dcinside 크롤링 실행 함수
from dcinside_crawler import get_url_dc, get_content_dc
import utility_module as util
#############################################################################
#                                 << 설정값 >>
keyword = "금양"       # 검색할 키워드
gall_name = "금융"    # 검색할 갤러리 선택하기

# 검색할 키워드(keyword)의 블랙리스트
# 목적에 맞지 않는 콘텐츠를 걸러내는 기능을 한다
blacklist = {
      "에코": ["에코백", "에코페", "에코팰", "에코플", "에코마", "에코디", "에코랜", "에코스", "에코하", "아마존 에코"]
    , "에코프로": ["http"]
    , "금양": ["http"]
    , "엘앤에프": ["http"]
    , "에스엠": ["http"]
    , "카카오": ["http"]
    , "lg화학": ["http"]
    , "토스": ["토스트", "도리토스", "치토스", "멘토스", "셀토스", "키보토스", "프로토스", "테스토스", "토스테론"]
}

# [갤러리 목록] "____" 갤러리
gall_url = {
      "미국주식": "https://gall.dcinside.com/mgallery/board/lists?id=stockus"
    , "해외주식": "https://gall.dcinside.com/mgallery/board/lists/?id=tenbagger"
    , "코스피": "https://gall.dcinside.com/mgallery/board/lists?id=kospi"
    , "국내선물옵션": "https://gall.dcinside.com/mini/board/lists/?id=koreafutures"
    , "실전주식투자": "https://gall.dcinside.com/mgallery/board/lists?id=jusik"
    , "나스닥": "https://gall.dcinside.com/mgallery/board/lists?id=nasdaq"
    , "다우": "https://gall.dcinside.com/mgallery/board/lists?id=dow100"
    , "슨피": "https://gall.dcinside.com/mini/board/lists/?id=snp500"
    , "금융": "https://gall.dcinside.com/mgallery/board/lists?id=finance"
    , "증권": "https://gall.dcinside.com/mgallery/board/lists/?id=securities"
    , "재테크": "https://gall.dcinside.com/mgallery/board/lists?id=jaetae"
    , "부동산": "https://gall.dcinside.com/board/lists/?id=immovables"
    , "신용카드": "https://gall.dcinside.com/board/lists/?id=creditcard"
    , "체크카드": "https://gall.dcinside.com/mgallery/board/lists?id=checkcard"
    , "캠퍼스개미": "https://gall.dcinside.com/mgallery/board/lists?id=smow"
    , "에너지주식": "https://gall.dcinside.com/mini/board/lists/?id=energystock"
    , "초전도체": "https://gall.dcinside.com/board/lists/?id=superconductor"
    , "편의점": "https://gall.dcinside.com/board/lists/?id=cs_new1"
    , "알뜰폰": "https://gall.dcinside.com/mgallery/board/lists?id=mvnogallery"
    , "SFF": "https://gall.dcinside.com/mgallery/board/lists?id=sff"
    , "토스": "https://gall.dcinside.com/mgallery/board/lists/?id=toss"
}

#############################################################################
#                              << 실행하는 곳 >>
get_url_dc(gall_url[gall_name], keyword, blacklist[keyword])        # [1. url 크롤링]
# get_content_dc(gall_url[gall_name], keyword, blacklist[keyword])    # [2. content 크롤링]

#############################################################################
#                                << 실험실 >>
# folder_path = f"./url/{keyword}"
# result_file_name = f"url_{keyword}_kakao"
# util.combine_csv_file(folder_path, result_file_name)
