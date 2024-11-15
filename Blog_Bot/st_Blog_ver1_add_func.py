import streamlit as st
from langchain_openai import ChatOpenAI

# 페이지 기본 설정
st.set_page_config(page_title="AI 블로그 작성 봇", page_icon="✍️", layout="wide")

# 사이드바 설정
st.sidebar.title("AI 블로그 작성 봇 설정")

# 사이드바 입력
# 블로그 스타일 설정
style = st.sidebar.selectbox("블로그 스타일을 선택하세요:", ["캐주얼", "전문적", "친근한", "유머러스한"])

# 블로그 길이 설정 (슬라이더)
length = st.sidebar.slider("블로그 길이를 선택하세요 (단어 수):", 300, 1500, 600, step=100)

# 대상 독자 설정
audience = st.sidebar.selectbox("대상 독자를 선택하세요:", ["초급", "중급", "전문가"])

# 블로그 주제 입력
topic = st.sidebar.text_input("블로그 주제를 입력하세요:", placeholder="예: 인공지능의 미래, 스마트 홈 기술, 요가의 건강상 이점 등")

if st.sidebar.button("작성 요청"):
    if topic.strip():
        # 블로그 포스트 생성 함수 호출
        llm = ChatOpenAI(temperature=0.7, model_name='gpt-4o-mini')
        prompt = f"Write a {style.lower()} blog post about: {topic}. The post should be around {length} words long. Target audience: {audience}."
        response = llm.predict(prompt)

        st.markdown(f"""
            <div style="background-color:#FAFAFA;padding:15px;border-radius:10px;margin-top:15px;">
                <h4>📝 생성된 블로그 포스트:</h4>
                <p>{response}</p>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.sidebar.warning("주제를 입력해주세요.")
else:
    # 기본 안내 메시지 표시
    st.markdown("""
        <div style="background-color:#F0F0F0;padding:15px;border-radius:10px;margin-top:15px;">
            <h4>📝 여기에 블로그 포스트가 생성됩니다:</h4>
            <p>사이드바에서 주제를 입력하고 <strong>작성 요청</strong> 버튼을 눌러주세요. 생성된 포스트가 이곳에 표시됩니다.</p>
        </div>
    """, unsafe_allow_html=True)

# 푸터 추가
st.markdown("""
    <div style="margin-top: 50px; padding: 15px; background-color: #444; color: white; text-align: center; border-radius: 10px;">
        <p>Powered by LangChain & OpenAI API | ✨ 당신의 블로그 작성을 더욱 편리하게.</p>
    </div>
""", unsafe_allow_html=True)
