import streamlit as st
from langchain_openai import ChatOpenAI

# 페이지 기본 설정
st.set_page_config(page_title="AI 블로그 작성 봇", page_icon="✍️", layout="wide")

# 사이드바 설정
st.sidebar.title("AI 블로그 작성 봇 설정")
st.sidebar.markdown("""
    이 도구는 블로그 작성을 돕기 위해 설계되었습니다. 원하는 주제를 입력하고 AI가 생성한 블로그 포스트를 확인해보세요!
""")

# 사이드바 입력
topic = st.sidebar.text_input("블로그 주제를 입력하세요:", placeholder="예: 인공지능의 미래, 스마트 홈 기술, 요가의 건강상 이점 등")
if st.sidebar.button("작성 요청"):
    if topic.strip():
        # 블로그 포스트 생성 함수 호출
        llm = ChatOpenAI(temperature=0.7, model_name='gpt-4o-mini')
        response = llm.predict(f"Write a blog post about: {topic}")
        st.markdown(f"""
            <div style="background-color:#FAFAFA;padding:15px;border-radius:10px;margin-top:15px;">
                <h4>📝 생성된 블로그 포스트:</h4>
                <p>{response}</p>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.sidebar.warning("주제를 입력해주세요.")

# 푸터 추가
st.markdown("""
    <div style="margin-top: 50px; padding: 15px; background-color: #444; color: white; text-align: center; border-radius: 10px;">
        <p>Powered by LangChain & OpenAI API | ✨ 당신의 블로그 작성을 더욱 편리하게.</p>
    </div>
""", unsafe_allow_html=True)
