# 경기대학교 3-2 분산 및 병렬 처리 프로젝트
--------
### 프로젝트 요구사항
![image](https://github.com/Hojun1123/3-2_Distributed_System/assets/65999992/a59ee0cb-4437-4462-b3f0-046bd86ac8bb)

### 주요 프로세스
1. BBC의 인터넷 기사 8,800개를 크롤링하여 /sourcedata에 텍스트 파일 생성
2. 해당 텍스트 데이터를 PC(1대, 2대, 4대)의 DB에 나누어 전송
3. 각 PC에서는 데이터에 전처리 및 Word Counting(NLTK 라이브러리 사용) 후, 결과를 클라이언트 PC로 전송
4. 모든 PC로 부터 Word Counting 결과가 도착하면, 작업 시간을 계산하고, Word Cloud를 출력

#### PC 1 대
![image](https://github.com/Hojun1123/3-2_Distributed_System/assets/65999992/4877efbf-c9bf-45e3-8c4f-e3211cedce4d)

#### PC 2 대
![image](https://github.com/Hojun1123/3-2_Distributed_System/assets/65999992/cf1fde49-6837-4154-9729-86ebbb348a21)

#### PC 4 대
![image](https://github.com/Hojun1123/3-2_Distributed_System/assets/65999992/4ee5fbb2-83db-4e1e-8d3b-e39f2ae20fd6)

-------
### 크롤링
![image](https://github.com/Hojun1123/3-2_Distributed_System/assets/65999992/03da0587-1c6e-4c69-9c4d-84c507cda373)
![image](https://github.com/Hojun1123/3-2_Distributed_System/assets/65999992/0485606f-4544-4570-bab5-0304d339fefc)
![image](https://github.com/Hojun1123/3-2_Distributed_System/assets/65999992/937a1482-b52f-42c9-bd29-b61439696d18)

### Word Counting(word_count.py, Server에서 수행)
텍스트(HTML) 데이터를 각 서버 PC로 전송을 마치면, Client는 전송 완료된 서버 PC에 대해 word_count.py를 원격 실행한다.
word_count는 아래와 같은 절차를 거친 후, Client에 DB에 [word, count] 형태로 결과를 전송한다.
![image](https://github.com/Hojun1123/3-2_Distributed_System/assets/65999992/05a0c8b2-8baf-455d-b685-058a902e0040)

### 실행 페이지
![image](https://github.com/Hojun1123/3-2_Distributed_System/assets/65999992/949cd3eb-076f-4bf9-bc76-5e01a6263378)

### 특이사항
![image](https://github.com/Hojun1123/3-2_Distributed_System/assets/65999992/4585942e-213b-48f1-a88e-c19b1e2bec28)
![image](https://github.com/Hojun1123/3-2_Distributed_System/assets/65999992/d20cc662-f54b-4173-b89a-b64c07f139b7)


