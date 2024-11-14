import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# 페이지 설정
st.set_page_config(
    page_title="LLM 에너지 최적화 모니터링 대시보드",
    layout="wide",
)

# 헤더
st.title("🔋 LLM 에너지 최적화 모니터링 대시보드")
st.markdown("실시간으로 LLM의 에너지 사용량과 최적화 상태를 모니터링합니다.")

# 사이드바 - 날짜 선택
st.sidebar.header("📅 날짜 필터(201601-201605)")
start_date = st.sidebar.date_input("시작 날짜", pd.to_datetime('2016-04-01'))
end_date = st.sidebar.date_input("종료 날짜", pd.to_datetime('2016-04-15'))

if start_date > end_date:
    st.sidebar.error("시작 날짜가 종료 날짜보다 늦을 수 없습니다.")

# 데이터 불러오기
@st.cache_data
def load_data(file_path):
    data = pd.read_csv(file_path, parse_dates=['date'], index_col='date')
    return data

# 사용자가 제공한 파일을 찾아서 데이터를 불러오는 시도에서의 file_path입니다.
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
col4.metric(label="현재 기온 수준", value=f"{current_optimization:.2f}")

# 푸터
st.markdown("---")
st.markdown("© LLM 모니터링 대시보드")
