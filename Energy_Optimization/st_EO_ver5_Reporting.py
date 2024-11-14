import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc
import os
from langchain_openai import ChatOpenAI
from langchain.document_loaders import PyPDFLoader

# LangChain과 OpenAI API 임포트
from langchain import PromptTemplate
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS

# 설치한 폰트 경로 설정
font_path = '/usr/share/fonts/truetype/nanum/NanumGothic.ttf'
font_name = font_manager.FontProperties(fname=font_path).get_name()
rc('font', family=font_name)
plt.rcParams['axes.unicode_minus'] = False

# 페이지 설정
st.set_page_config(page_title="LLM 에너지 최적화 모니터링 대시보드", layout="wide")

# 헤더
st.title("🔋 LLM 에너지 최적화 모니터링 대시보드")
st.markdown("실시간으로 LLM의 에너지 사용량과 최적화 상태를 모니터링합니다.")

# 사이드바 - 날짜 선택
st.sidebar.header("📅 날짜 필터")
start_date = st.sidebar.date_input("시작 날짜", pd.to_datetime('2016-04-01'))
end_date = st.sidebar.date_input("종료 날짜", pd.to_datetime('2016-04-15'))

if start_date > end_date:
    st.sidebar.error("시작 날짜가 종료 날짜보다 늦을 수 없습니다.")

# 데이터 불러오기
@st.cache_data
def load_data(file_path):
    data = pd.read_csv(file_path, parse_dates=['date'], index_col='date')
    return data

data = load_data("Energy_Optimization/data/KAG_energydata_complete.csv")

# 날짜 필터 적용
filtered_data = data[(data.index >= pd.to_datetime(start_date)) & (data.index <= pd.to_datetime(end_date))]

# 메인 열에서 레이아웃 설정
col1, col2 = st.columns(2)

# 에너지 사용량 추이 그래프
col1.subheader("⚡ 에너지 사용량 추이")
col1.line_chart(filtered_data['Appliances'])

# 최적화 수준 추이 그래프 (기온 데이터를 최적화 수준으로 사용)
col2.subheader("📈 기온 수준 추이")
col2.line_chart(filtered_data['T1'])

# 지표 표시
st.markdown("---")
st.header("현재 상태 지표")

col3, col4 = st.columns(2)
current_energy = filtered_data['Appliances'].iloc[-1]
current_optimization = filtered_data['T1'].iloc[-1]

col3.metric(label="현재 에너지 사용량 (Wh)", value=f"{current_energy:.2f}")
col4.metric(label="현재 최적화 수준 (기온)", value=f"{current_optimization:.2f}")

# 목표 설정값을 에너지 사용량 그래프에 선으로 표시
st.markdown("---")
st.header("평균 에너지 사용량과 목표 비교")
user_goal = st.sidebar.number_input("에너지 사용 목표 (Wh)", min_value=0, value=400, step=50)
fig2, ax2 = plt.subplots(figsize=(10, 6))
ax2.plot(filtered_data.index, filtered_data['Appliances'], label='에너지 사용량', color='blue')
ax2.axhline(y=user_goal, color='red', linestyle='--', label='사용자 목표')
ax2.set_ylabel("에너지 사용량 (Wh)")
ax2.set_title("에너지 사용량과 목표 비교")
ax2.legend()
st.pyplot(fig2)

# 시간대별 에너지 사용량 히트맵
st.markdown("---")
st.header("시간대별 에너지 사용량 히트맵")
fig, ax = plt.subplots(figsize=(10, 6))
pivot_data = filtered_data.copy()
pivot_data['hour'] = pivot_data.index.hour
pivot_data['day'] = pivot_data.index.date
pivot_table = pivot_data.pivot_table(index='hour', columns='day', values='Appliances', aggfunc='mean')
sns.heatmap(pivot_table, cmap="YlGnBu", ax=ax)
st.pyplot(fig)

# --- RAG 기능 추가 부분 시작 ---
st.markdown("---")
st.header("📊 데이터 분석 리포트")

# 데이터 분석 결과 요약 생성
def generate_analysis_summary(data):
    energy_mean = data['Appliances'].mean()
    energy_max = data['Appliances'].max()
    energy_min = data['Appliances'].min()
    temp_mean = data['T1'].mean()
    summary = f"""
    에너지 사용량의 평균은 {energy_mean:.2f}Wh 입니다.
    최대 에너지 사용량은 {energy_max:.2f}Wh 이며, 최소 사용량은 {energy_min:.2f}Wh 입니다.
    평균 실내 온도는 {temp_mean:.2f}°C 입니다.
    """
    return summary

# 그래프 데이터 요약 함수
def generate_graph_summary(data):
    # 에너지 사용량 추이 요약
    energy_trend = "에너지 사용량 추이에서 전반적으로 일정한 사용량이 유지되었으나, 일부 기간 동안 급격한 증가가 나타났습니다." \
                   if data['Appliances'].std() > 10 else "에너지 사용량이 일정하게 유지되고 있습니다."
    
    # 기온 수준 추이 요약
    temperature_trend = f"기온 수준의 평균은 {data['T1'].mean():.2f}°C로 유지되고 있습니다."

    # 히트맵 요약
    pivot_data = data.copy()
    pivot_data['hour'] = pivot_data.index.hour
    pivot_data['day'] = pivot_data.index.date
    pivot_table = pivot_data.pivot_table(index='hour', columns='day', values='Appliances', aggfunc='mean')
    highest_usage_hour = pivot_table.mean(axis=1).idxmax()
    heatmap_summary = f"시간대별 에너지 사용량 히트맵에서 가장 높은 사용량은 {highest_usage_hour}시에 나타났습니다."

    summary = f"""
    그래프 분석 요약:
    - {energy_trend}
    - {temperature_trend}
    - {heatmap_summary}
    """
    return summary

# 기존 데이터 분석 요약 생성
analysis_summary = generate_analysis_summary(filtered_data)

# 그래프 요약 생성
graph_summary = generate_graph_summary(filtered_data)

# 벡터 스토어에 저장할 문서 생성
data_docs = [analysis_summary, graph_summary]

# 임베딩 생성 및 벡터 스토어 구축
embeddings = OpenAIEmbeddings()
data_vectorstore = FAISS.from_texts(data_docs, embeddings)

# 사전에 정의된 문서 경로 목록
document_paths = ["Energy_Optimization/docs/data_description.pdf", 
                "Energy_Optimization/docs/optimization_paper.pdf"] # 여기서 경로를 설정하여 백엔드에서 문서를 가져옴
all_documents = []
for path in document_paths:
    if os.path.exists(path):
        loader = PyPDFLoader(path)
        data = loader.load()
        all_documents.extend(data)

doc_vectorstore = FAISS.from_documents(all_documents, embeddings)

# LLM 설정
llm = ChatOpenAI(temperature=0.7, model='gpt-4o-mini')

# 종합 에너지 사용량 분석 리포트 생성
st.subheader("📄 종합 에너지 사용량 분석 리포트")

# 문서에서 관련 내용 검색
query = "에너지 사용량 분석 보고서"
docs = doc_vectorstore.similarity_search(query, k=2)
doc_texts = "\n".join([doc.page_content for doc in docs])

# 프롬프트 템플릿 설정
prompt_template = PromptTemplate(
    input_variables=["analysis_summaries", "document_texts"],
    template="""
    당신은 에너지 데이터 분석 전문가입니다.
    아래는 에너지 데이터 분석 결과 요약입니다:

    {analysis_summaries}

    아래는 관련 문서들입니다:

    {document_texts}

    위의 내용을 바탕으로, 에너지 사용량에 대한 종합적인 분석 리포트를 작성해주세요.
    리포트에는 에너지 사용 추이, 패턴, 인사이트, 그리고 데이터를 기반으로 한 추천 사항을 포함해주세요.
    """
)

prompt = prompt_template.format(
    analysis_summaries=analysis_summary + "\n" + graph_summary,
    document_texts=doc_texts
)

# 리포트 생성
report = llm.predict(prompt)
st.write(report)

# 사용자 질문 입력
st.subheader("리포팅 서비스 관련 추가 질문:")
user_question = st.text_input("질문을 입력하세요", placeholder="예: 이번 기간 동안 에너지 사용 패턴은 어떠했나요?")

if user_question:
    # 유사한 문서(데이터 분석 결과) 검색
    docs = data_vectorstore.similarity_search(user_question)
    relevant_doc = docs[0]

    # 유사한 문서(참고 문서) 검색
    docs2 = doc_vectorstore.similarity_search(user_question)
    relevant_doc2 = docs2[0]

    # LLM을 사용하여 답변 생성
    prompt_template = PromptTemplate(
        input_variables=["context", "context2", "question"],
        template="""
        아래는 에너지 데이터 분석 결과입니다:

        {context}
        
        아래는 관련 문서 정보입니다:

        {context2}

        질문: {question}

        위의 내용을 바탕으로 질문에 대한 답변을 작성해주세요.
        """
    )
    prompt = prompt_template.format(context=relevant_doc, context2=relevant_doc2, question=user_question)
    answer = llm.predict(prompt)
    st.write("**답변:**")
    st.write(answer)
# --- RAG 기능 추가 부분 끝 ---

# 푸터
st.markdown("---")
st.markdown("© LLM 모니터링 대시보드")