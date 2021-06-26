# 책소개를 통한 카테고리 분류
![화면 캡처 2021-06-25 173855](https://user-images.githubusercontent.com/67940953/123511079-3bc59e00-d6ba-11eb-8936-a47a19e53747.png)

## 프로젝트 개요
알라딘 사이트에서 8개 카테고리를 선정해 selenium으로 크롤링, eunjeon의 Mecab으로 자연어 처리 후 tensorflow를 사용한 모델로 카테고리 예측
<br>

## 사용 언어
- python 3.7.10

## 개발 환경 및 사용 모듈
- numpy: 1.19.5
- pandas: 1.2.4
- selenium: 3.141.0
- eunjeon: 0.4.0
- scikit-learn: 0.24.2
- tenforflow: 2.5.0
- pyqt: 5.9.2

## 프로젝트 수행 방법
### 크롤링
알라딘 사이트에서 8개 카테고리를 선택해 크롤링한다. 이 때 사이트가 동적으로 이루어져있기 때문에 selenium을 사용하는데, 책 리스트에서 순서대로 책을 클릭한 후 책소개가 있는 곳까지 스크롤한 뒤 해당 내용과 책 제목을 저장한다.

카테고리별 크롤링된 파일은 data_concat.py 코드에서 하나의 파일로 concat해 저장한다.

### 전처리
책의 제목과 내용을 feature, 카테고리를 target으로 분리하고 target을 one-hot encoding한다. 이때 사용한 OneHotEncoder 객체는 추후 검증에 사용하기 위해 pickle을 사용해 저장한다.

feature는 자연어 처리를 진행하는데, eunjeon의 Mecab를 사용한다. 이번 프로젝트에선 형태소와 명사로 분류해보았으나 명사로 분류했을때 더 좋은 결과를 보였기 때문에 nouns를 사용해 전처리한 결과를 최종 모델에 학습시켰다. 분류한 뒤 stopword를 제거한 후 토큰화했다. 토큰화에 사용한 객체 또한 pickle로 저장하였다.

자연어 처리까지 마친 데이터는 각 행마다 길이가 다르기 때문에 가장 형태소 수가 많은 책을 기준으로 길이를 맞추었다. GRU을 진행하기 때문에 뒷쪽이 아닌 앞쪽에 0을 추가했다.

모든 전처리가 끝난 데이터는 npy 파일로 저장했다.

### 모델 레이어 구성
![image](https://user-images.githubusercontent.com/67940953/123511294-70862500-d6bb-11eb-9c3f-659e6692d1ee.png)
![image](https://user-images.githubusercontent.com/67940953/123511282-6401cc80-d6bb-11eb-95df-10e180432f67.png)


단어 벡터라이징에는 keras의 Embedding을 사용했다. 학습데이터 수가 차원의 수보다 적어져 성능이 저하되는 것을 막기 위해 output_dim을 적절히 조절했다.


주변 값과의 연관성을 분석하기 위해 Conv1D를 사용했으며, 동작에 영향을 주진 않지만 코드 형식을 통일하기 위해 MaxPool1D를 pool_size를 1로 설정한 뒤 사용했다.

또한 convolution 뒤 순환신경망 레이어인 GRU layer를 사용했다.

이렇게 모델을 학습시킨 결과 과적합이 발생했기 때문에 Dropout layer를 적절히 추가했다.

### GUI 구현
![image](https://user-images.githubusercontent.com/67940953/123511366-c9ee5400-d6bb-11eb-89c0-ccfe79433d0b.png)
gui는 pyqt5를 사용해 구현했다. 화면 및 기능은 위의 이미지와 같다.
기존에 저장해둔 모델과 pickle 파일들을 불러온 뒤 사용자가 입력한 문장을 분석해 결과를 출력한다.