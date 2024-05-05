# 경기대학교 3-2 분산 및 병렬 처리 프로젝트
--------
### 프로젝트 요구사항
![image](https://github.com/Hojun1123/3-2_Distributed_System/assets/65999992/a59ee0cb-4437-4462-b3f0-046bd86ac8bb)

### 주요 프로세스
1. BBC의 인터넷 기사 8,800개를 크롤링하여 /sourcedata에 텍스트 파일 생성
2. 해당 텍스트 데이터를 PC(1대, 2대, 4대)의 DB에 나누어 전송
3. 각 PC에서는 데이터에 전처리 및 Word Counting(NLTK 라이브러리 사용) 후, 결과를 클라이언트 PC로 전송
4. 모든 PC로 부터 Word Counting 결과가 도착하면, 작업 시간을 계산하고, Word Cloud를 출력


