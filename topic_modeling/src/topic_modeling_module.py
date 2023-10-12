import utility_module as util
from pykospacing import Spacing


####################################
# spacing_csv_content()
# 기능 : .csv 파일을 받아, 모든 'content'에 띄어쓰기 처리를 하고 결과 .csv를 만드는 함수
# 입력값 1 - rule_csv_file : spacing 규칙이 담겨있는 파일 이름
# 입력값 2 - target_csv_file : 띄어쓰기 처리할 csv 파일 이름
# 입력값 3 - csv_folder_path_ : csv 파일 모아둔 경로
@util.timer_decorator
def spacing_csv_content(rule_csv_file, target_csv_file, csv_folder_path_='./'):
    df = util.read_csv_file(target_csv_file, csv_folder_path_)  # 'df'에 파일 정보 저장
    print(df)
    print("[해당 df에 대하여 spacing을 진행하겠습니다]")
    spacing = Spacing(rules=[''])  # 띄어쓰기 처리의 준비작업
    spacing.set_rules_by_csv(f'./{rule_csv_file}', '단어')  # 규칙 설정

    df['spaced_content'] = df['content'].apply(spacing)  # 'content' 칼럼에 spacing 적용
    util.save_csv_file(df, f"spaced_{target_csv_file}", csv_folder_path_)
    print(f"[spaced_{target_csv_file} 파일로 저장되었습니다]")


########################
# 기능 : 한글 종성 있는지 판단하는 함수
def has_jongseong(char):
    if '가' <= char <= '힣':
        unicode_value = ord(char)
        jongseong = (unicode_value - 0xAC00) % 28
        return jongseong != 0
    else:
        return False