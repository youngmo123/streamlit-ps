import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc
import seaborn as sns
import os
from langchain_openai import ChatOpenAI


# 설치한 폰트 경로 설정
font_path = '/usr/share/fonts/truetype/nanum/NanumGothic.ttf'
font_name = font_manager.FontProperties(fname=font_path).get_name()
rc('font', family=font_name)
plt.rcParams['axes.unicode_minus'] = False


# 스트림릿 웹 애플리케이션 시작
def main():
    st.title('📊엑셀 데이터 업로드 및 시각화')
    
    # 엑셀 파일 업로드 (사이드바로 이동)
    uploaded_file = st.sidebar.file_uploader("📄엑셀 또는 CSV 파일을 업로드하세요", type=["xlsx", "xls", "csv"])
    
    if uploaded_file is not None:
        # 파일 형식에 따라 판다스로 읽기
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file, engine='openpyxl', header=0)
        
        # 인덱스 행을 제외한 데이터 표시 (여기서 인덱스는 첫 번째 행으로 가정)
        st.write("업로드한 파일의 데이터:")
        st.write(df)
        
        # 상관관계 히트맵 시각화 실행
        if st.button("상관관계 히트맵 시각화 실행"):
            numeric_df = df.select_dtypes(include=[np.number])  # 숫자형 데이터만 선택
            if numeric_df.empty:
                st.write("숫자형 데이터가 없습니다. 상관관계 히트맵을 생성할 수 없습니다.")
            else:
                fig, ax = plt.subplots(figsize=(10, 8))
                sns.heatmap(numeric_df.corr(), annot=True, cmap='YlGnBu', ax=ax)
                st.pyplot(fig)
        
        # 산점도 시각화 선택
        columns = df.columns.tolist()
        x_axis = st.selectbox('산점도 시각화 X축 선택', columns)
        y_axis = st.selectbox('산점도 시각화 Y축 선택', columns)
        
        # 간단한 시각화 (산점도)
        if st.button("산점도 시각화 실행"):
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.scatter(df[x_axis], df[y_axis])
            ax.set_xlabel(x_axis)
            ax.set_ylabel(y_axis)
            ax.set_title(f'{x_axis}와 {y_axis}의 산점도')
            
            st.pyplot(fig)

if __name__ == "__main__":
    main()
