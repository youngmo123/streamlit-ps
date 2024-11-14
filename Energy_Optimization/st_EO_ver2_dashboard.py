import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc

# 설치한 폰트 경로 설정
font_path = '/usr/share/fonts/truetype/nanum/NanumGothic.ttf'  # 도커에 설치한 폰트 경로
font_name = font_manager.FontProperties(fname=font_path).get_name()
rc('font', family=font_name)  # 'NanumGothic'으로 지정된 폰트 사용

# 마이너스 폰트 깨짐 방지
plt.rcParams['axes.unicode_minus'] = False

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
col4.metric(label="현재 최적화 수준 (기온)", value=f"{current_optimization:.2f}")

# 목표 설정값을 에너지 사용량 스택 그래프에 선으로 표시
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

# 푸터
st.markdown("---")
st.markdown("© LLM 모니터링 대시보드")