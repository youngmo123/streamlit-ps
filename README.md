# setting
커스텀 Dockerfile, requirements.txt 설정 확인

# testing
터미널 열고 streamlit hello 입력

# 패키지 추가 설치
버전에 맞는 pypi 검색 후, requirements.txt에 추가
(ex) pandas==2.2.3
텍스트 파일 저장 후
pip install -r requirements.txt

# Custom Chatbot Guide
## base 버전 실행: 기본 템플릿 제작
streamlit run custom_chatbot/st_chatbot_ver0_base.py
## session: 대화 기록이 남도록 세션 조정 / 최신 대화 기록이 위로 올라오도록 조정
streamlit run custom_chatbot/st_chatbot_ver1_session.py
streamlit run custom_chatbot/st_chatbot_ver1_session2.py
## history: 대화 요약 기억(Memory) 기능 추가
streamlit run custom_chatbot/st_chatbot_ver2_history.py
## add_func: ChatGPT Temperature 조정 슬라이더, 답변 스타일
streamlit run custom_chatbot/st_chatbot_ver3_add_func.py
## RAG: 사용자 업로드 파일에 대한 RAG / 추천 질문까지 추가
streamlit run custom_chatbot/st_chatbot_ver4_RAG.py
streamlit run custom_chatbot/st_chatbot_ver4_RAG2.py
## 강의 실습
기능 추가 예시 리스트
1. 소스 코드의 프롬프트 엔지니어링 수행 및, 헤더, 타이틀 등 텍스트나 레이아웃 등 전반적인 서비스 커스텀 수행
2. 대화 기록 저장 기능 추가 (excel, txt 확장자)
3. 이전 대화 내용이나 추천 질문에 따라 챗봇이 대화를 유도하거나 다음 질문을 제안할 수 있도록 기능 추가
4. 위의 기능 추가 예시를 참고하여 나만의 챗봇 커스텀해서 만들기, 위 내용은 프로젝트 문서에 내용으로 정리, 추후 개발하고 싶은 기능도 3가지 정도 제시

# Auto_QnA Guide
## base 버전 실행: 템플릿 제작
streamlit run Auto_QnA/st_QnA_ver0_base.py
## Layout: 레이아웃 스마트폰 채팅처럼 구현
streamlit run Auto_QnA/st_QnA_ver1_layout.py
## History: 대화 기록 세션, 메모리 구현되도록 개발
streamlit run Auto_QnA/st_QnA_ver2_history.py
## Multiple RAG: 백엔드에서 다중 문서 업로드 가능하도록 LangChain 기능 개발
streamlit run Auto_QnA/st_QnA_ver3_multi_RAG.py
## Question_REC: Vector Store로 등록된 문서에 대한 추천 질문 생성 / 간단한 프롬프트 수정으로 다음 추천 질문 생성
streamlit run Auto_QnA/st_QnA_ver4_Qustion_REC.py
streamlit run Auto_QnA/st_QnA_ver4_Qustion_REC2.py
## 강의 실습
1. 소스 코드의 프롬프트 엔지니어링 수행 및, 헤더, 타이틀 등 텍스트나 레이아웃 등 전반적인 서비스 커스텀 수행
2. 자동 언어 전환 기능: 고객이 질문을 작성할 때 사용하는 언어를 자동으로 감지해, 그 언어에 맞춰 AI가 응답하도록 하여 여러 언어를 자연스럽게 지원
3. 고객 만족도 평가 기능: 응답 후에 고객이 해당 답변에 만족했는지 평가할 수 있는 기능을 추가해, 평가 결과를 반영하여 모델의 응답 품질을 개선하는 데 활용
4. 고객 감정 분석 기능: 고객의 메시지에서 감정을 분석해 기쁨, 화남, 슬픔 등의 감정을 인식하도록 하여, 고객 만족도 평가 없이도 반응을 수집할 수 있도록 구현, 백엔드에서 로그 txt 형태나, csv 파일로 반응이 저장되도록 구성
5. 위의 기능 추가 예시를 참고하여 나만의 챗봇 커스텀해서 만들기, 위 내용은 프로젝트 문서에 내용으로 정리, 추후 개발하고 싶은 기능도 3가지 정도 제시

# Blog_Bot Guide
## base 버전 실행: 템플릿 제작
streamlit run Blog_Bot/st_Blog_ver0_base.py
## add_func: 블로그 좌측 사이드바에 다양한 기능 추가
streamlit run Blog_Bot/st_Blog_ver1_add_func.py
## SEO: 블로그 사이드바에 SEO 관련 기능 추가 (프롬프트 엔지니어링 기능)
streamlit run Blog_Bot/st_Blog_ver2_SEO.py
## Translation: 블로그 작성 후 다중 언어로 번역하는 기능 추가
streamlit run Blog_Bot/st_Blog_ver3_Translation.py
## Translation: 블로그 작성 후 SEO 피드백 기능 추가
streamlit run Blog_Bot/st_Blog_ver4_SEO2.py
## 강의 실습
1. 소스 코드의 프롬프트 엔지니어링 수행 및, 헤더, 타이틀 등 텍스트나 레이아웃 등 전반적인 서비스 커스텀 및 보완 수행
2. 블로그 포스트 편집 기능: 생성된 블로그 포스트를 텍스트 에디터에 불러와서 사용자가 직접 수정할 수 있도록 하는 기능을 추가
3. 자동 키워드 생성 및 삽입: SEO를 강화하기 위해, 주제에 따라 관련된 키워드를 AI 모델에 요청해 자동으로 추천하고, 해당 키워드를 블로그 포스트의 적절한 위치에 배치하는 기능을 추가
4. 표 자동 생성: 블로그 내용에서 표가 추가될 파트가 있으면 추가하는 프롬프트 및 streamlit 웹 구현
5. 위의 기능 추가 예시를 참고하여 나만의 챗봇 커스텀해서 만들기, 위 내용은 프로젝트 문서에 내용으로 정리, 추후 개발하고 싶은 기능도 3가지 정도 제시


# Energy_Optimization Guide
## base 버전 실행: 템플릿 제작
streamlit run Energy_Optimization/st_EO_ver0_template.py
## 데이터 연동: 실습 데이터 연결 및 모니터링 수행
streamlit run Energy_Optimization/st_EO_ver1_data.py
## 대시보드 고도화: 에너지 절감 목표 설정 및 시간별 사용량 히트맵 구현
streamlit run Energy_Optimization/st_EO_ver2_dashboard.py
## 데이터 분석 결과 RAG: 시각화 분석에서 산출된 결과값들 RAG 연동하여 리포트 형태로 구현
streamlit run Energy_Optimization/st_EO_ver3_Analysis_RAG.py
## 문서 RAG 연동 추가: 
streamlit run Energy_Optimization/st_EO_ver4_Docs_RAG.py
## 자동 리포팅 생성 기능 추가
streamlit run Energy_Optimization/st_EO_ver5_Reporting.py
## 강의 실습
1. 소스 코드의 프롬프트 엔지니어링 수행 및, 헤더, 타이틀 등 텍스트나 레이아웃 등 전반적인 서비스 커스텀 및 보완 수행
2. 에너지 최적화 관련으로 그래프 시각화 추가 (필요 시 ChatGPT로 아이디어 기획 활용)
ex: 상관관계 분석, 에너지사용량 분포 box plot, scatter plot 등
3. 세부 데이터 정보를 벡터스토어로 구축하고 RAG 추가 연동
4. 위의 기능 추가 예시를 참고하여 나만의 서비스 커스텀해서 만들기, 위 내용은 프로젝트 문서에 내용으로 정리, 추후 개발하고 싶은 기능도 3가지 정도 제시


# Meeting Summary
## 기본 템플릿 제작: 음성 파일 업로드 및 텍스트 변환
streamlit run Meeting_Summary/st_MS_ver0_template.py
## 시스템 최적화: CPU 컴퓨팅 작업을 위한 과부화 분산 및 최적화 수행
streamlit run Meeting_Summary/st_MS_ver1_optimization.py
## ChatGPT 회의록 요약 수행
streamlit run Meeting_Summary/st_MS_ver2_summary.py
## 프롬프트 엔지니어링: 회의록 요약문 구조화
streamlit run Meeting_Summary/st_MS_ver3_Prompt.py
## 강의 실습
1. 소스 코드의 프롬프트 엔지니어링 수행 및, 헤더, 타이틀 등 텍스트나 레이아웃 등 전반적인 서비스 커스텀 및 보완 수행
2. 회의록의 더욱 유용한 활용을 위한 추가 프롬프트 엔지니어링 작업
3. 회의록 작성의 스타일을 정의할 수 있는 다양한 부가기능 개발
4. 회의 세부 내용에 대해서 답변할 수 있는 챗봇 서비스 추가
5. 위의 기능 추가 예시를 참고하여 나만의 서비스 커스텀해서 만들기, 위 내용은 프로젝트 문서에 내용으로 정리, 추후 개발하고 싶은 기능도 3가지 정도 제시


# Streamlit Cloud Deployment 
## Custom 챗봇 앱 실행 확인

## Quick Start URL 확인
https://docs.streamlit.io/deploy/streamlit-community-cloud/get-started/quickstart
## 개발 환경에서 git 연동 및 push
 - 권한 부여 (터미널)
 git config --global --add safe.directory /workspaces/202411_Streamlit_LangChain
 - 로그인
 git config --global user.email "you@example.com"
 git config --global user.name "Your Name"
 - git 연동
 git remote add origin https://github.com/qruse/st_app_cloud.git
 - 파일 확인
 git status
 - 파일 추가
 git add .
 - git 커밋(업데이트 시 메시지 표시)
 git commit -m "first commit"
 - branch 설정(독립 작업 환경 설정)
 git branch -M main
 - git에 디렉토리 업로드
 git push -u origin main
## 개발환경에서 앱 실행 후 deploy 버튼 눌러서 편리하게 배포 가능
streamlit run custom_chatbot/st_chatbot_ver4_RAG2.py
## 아래 URL에서 앱 setting에서 secre_key 등록
https://share.streamlit.io/
## test2
streamlit run Energy_Optimization/st_EO_ver5_Reporting.py


# Next Step..!
1. Langserve 구축 및 Langsmith 연동
2. Streamlit 앱 최적화 수행
3. 각 모듈들을 도커 컨테이너로 개발
4. 도커 컴포즈를 통해 시스템 통합 빌드
5. CI/CD(Continuous Integration/Continuous Deployment) 구축
 - local: Jenkins 등 CI/CD 프레임워크 활용, 모니터링 시스템도 따로 프레임워크별로 개발
 - cloud: 기본적으로 클라우드 플랫폼에서는 CI/CD, 모니터링 시스템을 기본적으로 제공함
6. 호스팅 빌드 및 배포
% Streamlit은 Python 기반으로 매우 고수준 객체 단위로 개발되기 때문에 많은 사용자들
% 대상으로는 부적절할 수 있음. 프론트엔드에서의 React.js 등 프레임워크로 전환 필요