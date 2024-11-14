import streamlit as st  # Streamlit 라이브러리를 불러옴
from langchain_openai import ChatOpenAI

# 페이지 기본 설정
st.set_page_config(
    page_title="AI 기반 고객 응대 서비스",  # 브라우저 탭에 표시할 페이지 제목
    page_icon="🌐",  # 페이지 탭에 표시할 지구본 아이콘
    layout="wide"  # 페이지 레이아웃을 넓게 설정하여 다양한 정보 표시 가능
)

# 상단 헤더 설정
st.markdown("""
    <div style="background-color:#4A90E2;padding:10px;border-radius:10px;">
        <h1 style="color:white;text-align:center;"> 🤖 AI 고객 응대 서비스</h1>
    </div>
""", unsafe_allow_html=True)  # HTML로 상단 헤더 영역의 배경과 색상 스타일링

st.markdown("""
    <div style="padding: 10px;">
        <h3 style="color:#333; text-align:center;">AI와의 대화를 통해 고객님의 궁금증을 신속하게 해결해드리겠습니다.</h3>
        <p style="text-align:center;">문의사항을 아래에 입력하시고 <strong>보내기</strong> 버튼을 눌러주세요!</p>
    </div>
""", unsafe_allow_html=True)  # 페이지 안내 문구 표시

# ChatOpenAI 모델을 사용하여 답변 생성
def generate_response(input_text): 
    # ChatOpenAI 모델 인스턴스 생성
    llm = ChatOpenAI(
        temperature=1.0,  # 응답의 창의성을 최소화하여 일관성 있는 답변 제공
        model_name='gpt-4o-mini'  # 사전 지정된 AI 모델 사용
    )
    response = llm.predict(input_text)  # 사용자 입력을 바탕으로 AI 응답 생성
    st.markdown(f"""
        <div style="background-color:#F0F0F0;padding:15px;border-radius:10px;margin-top:15px;">
            <h4>💡 고객님께 드리는 답변:</h4>
            <p>{response}</p>
        </div>
    """, unsafe_allow_html=True)  # 응답을 표시 (스타일링 적용)

# 사용자 입력을 받는 폼 생성
with st.form("question_form"):  # 폼을 생성하여 사용자 질문을 받음
    text = st.text_area(
        "궁금한 점을 입력하세요:", 
        placeholder="예: 반품 정책은 어떻게 되나요?",
        height=150
    )  # 텍스트 입력 필드 생성
    submitted = st.form_submit_button("보내기", use_container_width=True)  # '보내기' 버튼 생성하여 폼 제출

    # 사용자가 질문을 제출했을 때 답변 생성
    if submitted:  # 폼이 제출되었는지 확인
        if text.strip():
            generate_response(text)  # 사용자의 입력 텍스트로 응답 생성 함수 호출
        else:
            st.warning("질문을 입력해주세요.")

# 푸터 추가
st.markdown("""
    <div style="margin-top: 50px; padding: 15px; background-color: #333; color: white; text-align: center; border-radius: 10px;">
        <p>Powered by LangChain & OpenAI API | 🏦 고객의 만족을 위해 언제나 최선을 다합니다.</p>
    </div>
""", unsafe_allow_html=True)  # 페이지 하단에 푸터 표시 (스타일링 적용)