import streamlit as st
from langchain_openai import ChatOpenAI

# 페이지 기본 설정
st.set_page_config(page_title="AI 블로그 작성 봇", page_icon="✍️", layout="wide")

# 세션 상태 초기화
if 'response' not in st.session_state:
    st.session_state.response = ''
if 'translation' not in st.session_state:
    st.session_state.translation = ''
if 'target_language' not in st.session_state:
    st.session_state.target_language = '영어'

# 사이드바 설정
st.sidebar.title("AI 블로그 작성 봇 설정")

# 사이드바 입력
# 블로그 주제 입력
topic = st.sidebar.text_input("블로그 주제를 입력하세요:", placeholder="예: 인공지능의 미래, 스마트 홈 기술, 요가의 건강상 이점 등")

# 블로그 스타일 설정
style = st.sidebar.selectbox("블로그 스타일을 선택하세요:", ["캐주얼", "전문적", "친근한", "유머러스한"])

# 블로그 길이 설정 (슬라이더)
length = st.sidebar.slider("블로그 길이를 선택하세요 (단어 수):", 300, 1500, 600, step=100)

# 대상 독자 설정
audience = st.sidebar.selectbox("대상 독자를 선택하세요:", ["초급", "중급", "전문가"])

# SEO 최적화 설정
st.sidebar.markdown("### SEO 최적화 설정")
st.sidebar.markdown("<small>아래 옵션들은 블로그의 검색 노출에 도움을 줄 수 있습니다.</small>", unsafe_allow_html=True)

# 키워드 밀도 조절
seo_keyword_density = st.sidebar.checkbox("키워드 밀도 조절 활성화")
st.sidebar.markdown("<small>블로그에서 주요 키워드를 적절히 반복하여 검색 엔진에 잘 노출되도록 합니다.</small>", unsafe_allow_html=True)

# 메타 태그 생성
seo_meta_tags = st.sidebar.checkbox("메타 태그 생성 활성화")
st.sidebar.markdown("<small>검색 엔진에서 블로그를 잘 이해하도록 메타 설명과 태그를 자동으로 생성합니다.</small>", unsafe_allow_html=True)

# 관련 질문 및 키워드 추천
seo_related_questions = st.sidebar.checkbox("관련 질문 및 키워드 추천 추가")
st.sidebar.markdown("<small>블로그 주제와 관련된 자주 묻는 질문과 추가 키워드를 포함하여 SEO를 강화합니다.</small>", unsafe_allow_html=True)

# URL 슬러그 최적화
seo_url_slug = st.sidebar.checkbox("URL 슬러그 최적화 활성화")
st.sidebar.markdown("<small>블로그 제목을 기반으로 검색에 유리한 짧고 간결한 URL을 제안합니다.</small>", unsafe_allow_html=True)

# 헤더 태그 구조화
seo_header_tags = st.sidebar.checkbox("헤더 태그 구조화 활성화")
st.sidebar.markdown("<small>블로그 포스트에 적절한 H1, H2, H3 태그를 추가하여 구조를 명확히 합니다.</small>", unsafe_allow_html=True)

# 블로그 포스트 생성
if st.sidebar.button("작성 요청"):
    if topic.strip():
        # 블로그 포스트 생성 함수 호출
        llm = ChatOpenAI(temperature=0.7, model_name='gpt-4o-mini')
        prompt = f"Write a {style.lower()} blog post about: {topic}. The post should be around {length} words long. Target audience: {audience}."

        # SEO 설정에 따라 프롬프트 수정
        if seo_keyword_density:
            prompt += " Ensure to maintain an optimal keyword density for SEO."
        if seo_meta_tags:
            prompt += " Generate suitable meta tags for the blog post."
        if seo_related_questions:
            prompt += " Include related questions and suggested keywords."
        if seo_url_slug:
            prompt += " Suggest an optimized URL slug for the topic."
        if seo_header_tags:
            prompt += " Structure the content with appropriate header tags (H1, H2, H3)."

        response = llm.predict(prompt)
        st.session_state.response = response  # 세션 상태에 저장
        st.session_state.translation = ''  # 새로운 포스트 생성 시 번역 초기화

    else:
        st.sidebar.warning("주제를 입력해주세요.")

# 생성된 블로그 포스트 표시
if st.session_state.response:
    st.markdown(f"""
        <div style="background-color:#FAFAFA;padding:15px;border-radius:10px;margin-top:15px;">
            <h4>📝 생성된 블로그 포스트:</h4>
            <p>{st.session_state.response}</p>
        </div>
    """, unsafe_allow_html=True)

    # 다국어 번역 기능 추가
    st.markdown("### 번역 옵션")
    target_language = st.selectbox("번역할 언어를 선택하세요:", ["영어", "중국어", "일본어", "스페인어", "아랍어", "힌디어", "프랑스어", "러시아어"])
    st.session_state.target_language = target_language  # 선택된 언어 저장

    if st.button("번역 요청"):
        llm = ChatOpenAI(temperature=0.7, model_name='gpt-4o-mini')
        translation_prompt = f"Translate the following text into {target_language}: {st.session_state.response}"
        translation_response = llm.predict(translation_prompt)
        st.session_state.translation = translation_response  # 세션 상태에 저장

    # 번역 결과 표시
    if st.session_state.translation:
        st.markdown(f"""
            <div style="background-color:#E8F5E9;padding:15px;border-radius:10px;margin-top:15px;">
                <h4>🌍 번역된 블로그 포스트 ({st.session_state.target_language}):</h4>
                <p>{st.session_state.translation}</p>
            </div>
        """, unsafe_allow_html=True)
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
