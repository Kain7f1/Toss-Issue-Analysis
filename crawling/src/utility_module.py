from calendar import monthrange
from datetime import datetime
import pandas as pd
import os
import re


# 입력 : 2000.01.01 형식을 입력받아서
# return : 그 달의 마지막 날짜를 리턴
def get_last_date(date_string):
    date_format = "%Y.%m.%d"    # 날짜 형식 (예: 2023.01.01)
    date_object = datetime.strptime(date_string, date_format)
    _, last_day = monthrange(date_object.year, date_object.month)
    return f"{date_object.year}.{date_object.month:02d}.{last_day:02d}"


def make_date_range(year, month):
    last_date = get_last_date(f'{year}.{month}.01')
    date_list = []
    for day in range(1, 30, 3):
        day_to = day + 2
        if day == 28:
            day_to = int(last_date[-2:])
        date_list.append([f'{year}.{month}.{day:02d}', f'{year}.{month}.{day_to:02d}'])
    return date_list


# 기능 : 폴더를  생성한다
# 입력값 : 파일 경로(이름)
def create_folder(folder_path):
    # 폴더가 존재하지 않는 경우, 폴더 생성
    if os.path.exists(folder_path):
        print("폴더가 이미 존재합니다.")
    else:
        os.makedirs(folder_path)
        print(f"폴더 : {folder_path}를 만들었습니다.")
    print("create_folder()를 종료합니다")


# 입력값 : folder_path, endswith (파일이름의 검색조건 : 파일명의 끝)
# file_names 리스트를 가져오는 함수
def load_file_names(folder_path, endswith='url.csv'):
    files = []
    # 폴더 내의 모든 파일을 탐색
    print(f"load_files() : {folder_path} 내의 파일을 탐색합니다. 검색조건 : endswith={endswith}")
    for filename in os.listdir(folder_path):
        if filename.endswith(endswith):
            files.append(filename)

    print("load_files()의 결과는 다음과 같습니다. ")
    for file in files:
        print(file)
    print("load_files()을 종료합니다")
    return files


# df 내용을 읽어옴
# return : df
def read_file(folder_path, file_name):
    combined_path = os.path.join(folder_path, file_name)        # os.path.join()을 사용하여 두 경로를 합칩니다.
    return pd.read_csv(combined_path, encoding='utf-8')


# df의 내용을 folder/file 로 저장
def save_file(df, folder_path, file_name):
    combined_path = os.path.join(folder_path, file_name)        # os.path.join()을 사용하여 두 경로를 합칩니다.
    df.to_csv(combined_path, encoding='utf-8', index=False)     # df의 내용을 csv 형식으로 저장합니다


def preprocess_content(input_str):
    return re.sub(r'[^\w\s.]|\d', ' ', input_str)


def preprocess_file(keyword):
    folder_path = f"./{keyword}"
    content_file_names = load_file_names(folder_path, endswith='content.csv')
    print(f'preprocess_file({keyword})를 진행합니다')
    for content_file_name in content_file_names:
        preprocessed_file_name = f"{content_file_name[:-4]}_preprocessed.csv"   # 저장할 파일 이름
        df = read_file(folder_path, file_name=content_file_name)    # 파일 읽어오기
        df['content'] = df['content'].astype(str)
        df['content'] = df['content'].apply(preprocess_content)     # 전처리
        df = df.loc[df['content'].shift() != df['content']]         # 중복되는 행 지우기
        # csv로 만든다
        save_file(df, folder_path, file_name=preprocessed_file_name)
        print(f"[종료] : {content_file_name} 파일의 content로부터 {preprocessed_file_name} 파일을 만들었습니다")


def combine_content_file(keyword):
    content_file_names = load_file_names(f"./{keyword}/content", endswith='content.csv')
    result_file_name = f"{keyword}_content.csv"
    dataframes = []
    print(f'combine_content_file({keyword})를 진행합니다')
    for content_file_name in content_file_names:
        df_content = read_file(f"./{keyword}/content", file_name=content_file_name)
        dataframes.append(df_content)
    merged_df = pd.concat(dataframes)
    print(merged_df.head())
    print(merged_df.tail())
    merged_df.dropna(inplace=True)
    # csv로 만든다
    save_file(merged_df, f"./{keyword}", file_name=result_file_name)
    print(f"[종료] content 파일들을 하나로 합쳤습니다.")


def is_korean(s):
    return bool(re.fullmatch("[\u3131-\u3163\uAC00-\uD7A3]+", s))


# input_list의 원소에 criteria 의 원소 중 하나라도 있으면 True, 아니면 False
def check_criteria(input_list, criteria):
    return any(element in input_list for element in criteria)


def remove_stopword(keyword):
    # 파일 열기
    folder_path = f'./{keyword}'
    file_name = f'{keyword}_content_tokenized.csv'
    with open('stopwords.txt', 'r', encoding='utf-8') as file:
        # 라인별로 읽어 리스트로 저장
        stopwords = file.readlines()
    stopwords = [word.strip() for word in stopwords]
    print('stopwords.txt 를 불러왔습니다')

    df = read_file(folder_path, file_name)
    print(f'{file_name} 를 불러왔습니다')
    for stopword in stopwords:
        df['content'] = df['content'].str.replace(f'\\b{stopword} \\b', '', regex=True)
    print('stopwords를 지웠습니다')

    save_file(df, folder_path, f'{keyword}_content_tokenized_removed_stopwords.csv')
    print(f'{keyword}_removed_stopwords.csv 파일을 저장했습니다')


def dropna_and_save(file_path):
    df = pd.read_csv(file_path, encoding='utf-8')
    df.dropna(inplace=True)
    df.to_csv(file_path, encoding='utf-8', index=False)


# 목적 : 에러 로그를 읽고, 에러가 있으면 csv 파일을 만든다
def error_check(error_log, folder_path, file_name):
    # error 발생 했는지 확인
    if len(error_log) > 0:
        print("[에러 발생 로그 입니다]")
        for error in error_log:
            print(error)      # 에러 로그 출력
        df_error = pd.DataFrame(error_log)   # df 생성
        error_file_path = os.path.join(folder_path, f"{file_name}_error.csv")
        df_error.to_csv(error_file_path, encoding='utf-8', index=False)
        print("[에러 발생 로그를 파일로 저장함]")
    else:
        print("[에러 없음]")


# 목적 : title 텍스트를 전처리한다
# 기능 : 끝에붙은 대괄호와 안의 숫자, 콤마 (","), "u\202c" 를 제거한다
def preprocess_title(text):
    result = re.sub(r'\[\d+\]$', '', text).replace("\u202c", "").replace(',', '').strip()
    if len(result) == 0:
        return "_"
    else:
        return result

def preprocess_content(text):
    result = text.replace("- dc official App", "").replace("- dc App", "").replace(',', '').strip()
    if len(result) == 0:
        return "_"
    else:
        return result

