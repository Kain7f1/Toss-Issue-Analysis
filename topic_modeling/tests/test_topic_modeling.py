import topic_modeling_module as btm
import utility_module as util
################################################
# 2-a) 크롤링한 파일 불러오기
# {step 1} topic_modeling/tests 폴더에 합칠 .csv파일들을 넣어주세요
# {step 2} combine_crawling_results() 함수를 실행한다

# combine_crawling_results()


################################################
# 2-b) 감성분석 (paused)


################################################
# 2-c) 형태소 분석
text = "형들 신린이 질문 오지게 박습니다 알바하는 대학생인데 하이브리드 카드 발급 가능한가요? 토스 신용등급 보니까 779정도 나와용 그리고 카드 발급하고 집으로 오는거 말고 방문수령도 가능한가요?"


################################################
# 2-d) 토픽모델링


################################################
# 2-e) 불용어 처리


################################################
# 크롤링 결과를 합치는 함수
def combine_crawling_results():
    folder_path = "./"
    result_file_name = "crawling_result"    # 결과 파일 이름
    util.combine_csv_file(folder_path, result_file_name)
