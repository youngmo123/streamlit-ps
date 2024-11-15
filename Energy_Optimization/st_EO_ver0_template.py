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
st.sidebar.header("📅 날짜 필터")
start_date = st.sidebar.date_input("시작 날짜", datetime.now() - timedelta(days=7))
end_date = st.sidebar.date_input("종료 날짜", datetime.now())

if start_date > end_date:
    st.sidebar.error("시작 날짜가 종료 날짜보다 늦을 수 없습니다.")

# 예시 데이터 생성
@st.cache_data
def load_data():
    dates = pd.date_range(start=datetime.now() - timedelta(days=30), periods=720, freq='H')
    energy_usage = np.random.uniform(50, 150, size=(720,))
    optimization_level = np.random.uniform(70, 100, size=(720,))
    data = pd.DataFrame({
        '날짜': dates,
        '에너지 사용량 (kWh)': energy_usage,
        '최적화 수준 (%)': optimization_level
    })
    return data

data = load_data()

# 날짜 필터 적용
filtered_data = data[(data['날짜'] >= pd.to_datetime(start_date)) & (data['날짜'] <= pd.to_datetime(end_date))]

# 메인 영역 - 열 레이아웃
col1, col2 = st.columns(2)

# 에너지 사용량 추이 그래프
col1.subheader("⚡ 에너지 사용량 추이")
col1.line_chart(filtered_data.set_index('날짜')['에너지 사용량 (kWh)'])

# 최적화 수준 추이 그래프
col2.subheader("📈 최적화 수준 추이")
col2.line_chart(filtered_data.set_index('날짜')['최적화 수준 (%)'])

# 지표 표시
st.markdown("---")
st.header("현재 상태 지표")

col3, col4 = st.columns(2)
current_energy = filtered_data['에너지 사용량 (kWh)'].iloc[-1]
current_optimization = filtered_data['최적화 수준 (%)'].iloc[-1]

col3.metric(label="현재 에너지 사용량 (kWh)", value=f"{current_energy:.2f}")
col4.metric(label="현재 최적화 수준 (%)", value=f"{current_optimization:.2f}")

# 푸터
st.markdown("---")
st.markdown("© LLM 모니터링 대시보드")