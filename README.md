# Toss-Issue-Analysis

---

## Toss 이슈 분석 프로젝트

### 요구사항  
* Toss 업데이트의 시장 반응을 한 눈에 파악하고 싶다

### 가설설정
* 익명성을 띤 온라인 커뮤니티에서는, 사용자의 앱 사용 경험이 직설적으로 표현될 것이다.

### 프로세스
1. 한국 최대 커뮤니티 DCinside의 약 8만 건의 부정적/긍정적 text를 수집한다
2. 주 별로, 어떤 이슈가 화제가 되었는지 분석한다
3. 분석 결과를 그래프로 시각화하여, 사용자가 직관적으로 파악할 수 있도록 한다

### 역할 분배 : 팀 안티프래질 (Team Antifragile)
장소희 : 팀장, 데이터 시각화, UI/UX 디자인  
이한솔 (본인) : [크롤러](https://github.com/Kain7f1/DC-Crawler) 제작, 데이터 분석, 프로젝트/노션 관리  
전인호 : 프로젝트 기획

### 협업 Tool
* [Notion](https://kain7f1.notion.site/Toss-Image-Enhancement-96a129fbd90f4bf39a94e800fc451e9f)
* [GitHub](https://github.com/Kain7f1/Toss-Issue-Analysis)

### 개발 Tool
* Python 개발환경 : Pycharm 
* 데이터 시각화 도구 : Tableau

---

## 0. 프로젝트 결과 요약

![a.png](image_files%2Fa.png)

### 1. 지난 1주 동안의 데이터 시각화 : 워드클라우드, 원그래프, 막대그래프, 선그래프
> 워드클라우드 : 단어 빈도수에 비례하여 단어 크기가 커지게 함으로써, 어떤 이슈가 주목받았는지 직관적으로 알 수 있다.  
> 원그래프 : 빈도수에 따라 시각화한다.  
> 막대그래프 : 빈도수 상위 3개 토픽의 언급량을 보여준다.  
> 선그래프 : 7일동안의 빈도수 변화를 파악할 수 있다. (빈도수 상위 3개 토픽)

![b.png](image_files%2Fb.png)

### 2. 이머징 이슈, 핫이슈 시각화 : 그래프
> 이머징 이슈 : 지난 주에 비해, 언급량이 증가한 이슈  
> 핫이슈 : 언급량이 절대적으로 많은 이슈
#### - 각 포인트를 클릭하면, 우측의 뉴스 검색 결과가 연동되어 표시되도록 하였다. 
#### - 사용자는 이를 통해 실제로 어떤 사건이 있었는지 빠르게 파악할 수 있다

---

# 프로젝트 진행 과정

## 차례
1. 프로젝트 기획
2. 크롤링
3. 전처리
4. 단어 추출 및 토큰화
5. 토픽모델링
6. 데이터 분석
7. 시각화
8. 총평

---

## 1. 프로젝트 기획
![1.png](image_files%2F1.png)
![2.png](image_files%2F2.png)
![3.png](image_files%2F3.png)

## 2. 크롤링

![4.png](image_files%2F4.png)
![5.png](image_files%2F5.png)

## 3.전처리

![6.png](image_files%2F6.png) 

## 4. 단어 추출 및 토큰화

![7.png](image_files%2F7.png)

## 5. 토픽모델링

![8.png](image_files%2F8.png)

## 6. 데이터 분석

![11.png](image_files%2F11.png)

![13.png](image_files%2F13.png)

## 7. 시각화

![a.png](image_files%2Fa.png)
![b.png](image_files%2Fb.png)
![c.png](image_files%2Fc.png)

## 8. 총평
![99.png](image_files%2F99.png)
