import topic_modeling_module as tp
import utility_module as util
from pykospacing import Spacing
import pandas as pd
from soynlp.utils import DoublespaceLineCorpus
from soynlp.noun import LRNounExtractor_v2

################################################
# 0. 세팅
# csv_file_path = "./csv_files/toss_from_2020.csv"               # 크롤링 결과 .csv 파일의 경로
# df = pd.read_csv(csv_file_path, encoding='utf-8')    # 크롤링 결과 .csv 파일을 불러옵니다
# print(df)

################################################
# 1. 감성분석 (paused)


################################################
# 2. 띄어쓰기 처리

# [설정값] --------------------------------------------------------------------#
spacing_rule_csv = "spacing_rule_toss.csv"  # spacing 규칙이 담겨있는 파일 이름
csv_file = "toss_from_2020.csv"             # 띄어쓰기 처리할 csv 파일 이름
csv_folder_path = "./csv_files"                 # csv 파일 모아둔 경로

# [실행함수] ------------------------------------------------------------------#
# 띄어쓰기 된 칼럼 'spaced_content'를 추가하여 .csv 파일을 저장한다
# tp.spacing_csv_content(spacing_rule_csv, csv_file, csv_folder_path)


################################################
# 3. 토큰화
# [파일 이름 설정] -----------------------------------------------------
spaced_file_path = "./csv_files/spaced_toss_from_2020.csv"   # spacing .csv 파일의 경로
doublespace_file_path = "./doublespace_toss_from_2020.txt"

# [실행 함수]
# tp.make_doublespace_txt_from_spaced_csv(spaced_file_path, doublespace_file_path)


################################################
# 4. 토픽모델링
# [lda 설정값] -----------------------------------------------------
min_df = 10
n_components = 100
max_iter = 1
str_min_df = str(min_df).replace(".", "")
# [파일 이름 설정] -----------------------------------------------------
lda_folder_path = "./lda_files"
lda_file_path = f"lda_model_{str_min_df}_{n_components}_{max_iter}.pkl"   # spacing .csv 파일의 경로
tokenized_file = "outliers_removed_tokenized_toss.csv"

tp.fit_and_save_lda_model(csv_file_path=tokenized_file,
                          csv_folder_path=csv_folder_path,
                          save_file_path=lda_file_path,
                          save_folder_path=lda_folder_path,
                          min_df=min_df,
                          n_components=n_components,
                          max_iter=max_iter
                          )


################################################
# 5. 불용어 처리
