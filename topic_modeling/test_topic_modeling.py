from topic_modeling_module import spacing_csv_content
import utility_module as util
from pykospacing import Spacing
import pandas as pd


################################################
# 0. 세팅
# csv_file_path = "./csv/toss_from_2020.csv"               # 크롤링 결과 .csv 파일의 경로
# df = pd.read_csv(csv_file_path, encoding='utf-8')    # 크롤링 결과 .csv 파일을 불러옵니다
# print(df)

################################################
# 1. 감성분석 (paused)


################################################
# 2. 띄어쓰기 처리

# [설정값] --------------------------------------------------------------------#
spacing_rule_csv = "spacing_rule_toss.csv"  # spacing 규칙이 담겨있는 파일 이름
csv_file = "toss_from_2020.csv"             # 띄어쓰기 처리할 csv 파일 이름
# csv_file = "temp.csv"
csv_folder_path = "./csv_files"                 # csv 파일 모아둔 경로

# [실행함수] ------------------------------------------------------------------#
# 띄어쓰기 된 칼럼 'spaced_content'를 추가하여 .csv 파일을 저장한다
spacing_csv_content(spacing_rule_csv, csv_file, csv_folder_path)


################################################
# 3. 형태소 분석


################################################
# 4. 토픽모델링


################################################
# 5. 불용어 처리
