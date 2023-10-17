from pykospacing import Spacing
from soynlp.normalizer import emoticon_normalize
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
import re
import joblib
import pandas as pd
import utility_module as util


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


###########################
# 기능 : spaced .csv 파일을 받아 doublespace .txt 파일을 만든다
# input_path : spacing 결과 .csv 파일의 경로
# output_path : doublespace .txt 파일의 경로
@util.timer_decorator
def make_doublespace_txt_from_spaced_csv(input_path, output_path):
    print(f"[{input_path} 파일을 doublespace 처리 하겠습니다]")
    df = pd.read_csv(input_path, encoding='utf-8')  # spacing 결과 .csv 파일을 불러옵니다
    # 'content' 칼럼의 문자열에 emoticon_normalize 적용
    df['spaced_content'] = df['spaced_content'].apply(lambda x: emoticon_normalize(x, num_repeats=3))
    # space된 content 불러오고, "?"을 제외한 특수문자를 없앤다
    spaced_content = df['spaced_content'].apply(lambda x: re.sub(r'[^\w\s\?]', '', x))
    # doublespace 처리
    merged_text = '  \n'.join(spaced_content)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(merged_text)                    # 파일 저장
    print(f"[{output_path} 파일을 만들었습니다]")


########################
# 기능 : 한글 종성 있는지 판단하는 함수
def has_jongseong(char):
    if '가' <= char <= '힣':
        unicode_value = ord(char)
        jongseong = (unicode_value - 0xAC00) % 28
        return jongseong != 0
    else:
        return False


##########################
# lda 모델을 학습하고 저장하는 함수
@util.timer_decorator
def fit_and_save_lda_model(csv_file_path, csv_folder_path, save_file_path, save_folder_path, min_df, n_components, max_iter):
    df = util.read_csv_file(csv_file_path, csv_folder_path)
    # It looks like we lost the variable `texts_with_bigrams` as well.
    # Let's start from extracting the 'tokens_with_bigrams' again and proceed to LDA modeling.

    # Extract tokens_with_bigrams from the DataFrame
    token_with_bigram_lists = df['tokens_with_bigrams'].apply(eval).tolist()

    # Convert the list of tokens to text data
    texts_with_bigrams = [' '.join(tokens) for tokens in token_with_bigram_lists]

    # Use CountVectorizer to transform the text data to a term frequency (TF) matrix
    print("vectorizer 하겠습니다")
    vectorizer = CountVectorizer(max_df=0.95, min_df=min_df)
    X_with_bigrams = vectorizer.fit_transform(texts_with_bigrams)

    # Create and train LDA model with 100 topics
    lda_model = LatentDirichletAllocation(
        n_components=n_components,  # 토픽의 수
        doc_topic_prior=0.01,  # 알파 값
        max_iter=max_iter,  # 반복 횟수
        n_jobs=-1,
        verbose=1
    )
    print("lda model을 학습하겠습니다.")
    lda_model.fit(X_with_bigrams)   # 모델 학습

    joblib.dump(lda_model, f"{save_folder_path}/{save_file_path}")