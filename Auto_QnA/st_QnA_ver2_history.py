import streamlit as st  # Streamlit 라이브러리를 불러옴
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationSummaryMemory

# 페이지 기본 설정
st.set_page_config(
    page_title="AI 기반 고객 응대 서비스",  # 브라우저 탭에 표시할 페이지 제목
    page_icon="🌐",  # 페이지 탭에 표시할 지구본 아이콘
    layout="centered"  # 페이지 레이아웃을 중앙에 정렬하여 모바일 채팅 스타일로 구성
)

# 대화 히스토리 초기화
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []  # 대화 히스토리용 리스트 초기화

# 상단 헤더 설정
st.markdown("""
    <div style="background-color:#4A90E2;padding:10px;border-radius:10px;">
        <h1 style="color:white;text-align:center;"> 🤖 AI 고객 응대 서비스</h1>
    </div>
""", unsafe_allow_html=True)  # HTML로 상단 헤더 영역의 배경과 색상 스타일링

# 채팅 스타일의 UI 구성
# ChatOpenAI 모델을 사용하여 답변 생성 및 메모리 추가
def generate_response(input_text): 
    # ChatOpenAI 모델 인스턴스 생성
    llm = ChatOpenAI(
        temperature=1.0,  # 응답의 창의성을 최소화하여 일관성 있는 답변 제공
        model_name='gpt-4o-mini'  # 사전 지정된 AI 모델 사용
    )
    
    # ConversationSummaryMemory 설정 (토큰 크기 제한)
    if "memory" not in st.session_state:
        st.session_state["memory"] = ConversationSummaryMemory(llm=llm, max_token_limit=500)  # 최대 500 토큰으로 제한
    
    # 대화 히스토리를 메모리에서 가져와 프롬프트에 반영
    memory_summary = st.session_state["memory"].load_memory_variables({})["history"]
    full_input = f"{memory_summary}\nUser: {input_text}\nAI:"
    response = llm.predict(full_input)  # 사용자 입력을 바탕으로 AI 응답 생성
    
    # 대화 히스토리를 메모리에 저장
    st.session_state["memory"].save_context({"input": input_text}, {"output": response})
    
    return response  # 응답 반환

# 사용자 입력을 받는 폼 생성
with st.form("question_form"):  # 폼을 생성하여 사용자 질문을 받음
    text = st.text_input(
        "궁금한 점을 입력하세요:", 
        placeholder="예: 반품 정책은 어떻게 되나요?",
    )  # 텍스트 입력 필드 생성
    submitted = st.form_submit_button("보내기", use_container_width=True)  # '보내기' 버튼 생성하여 폼 제출

    # 사용자가 질문을 제출했을 때 답변 생성
    if submitted and text.strip():
        response = generate_response(text)  # 응답 생성 함수 호출
        st.session_state["chat_history"].append(("User", text))  # 사용자 입력을 대화 히스토리에 추가
        st.session_state["chat_history"].append(("AI", response))  # AI 응답을 대화 히스토리에 추가
    elif submitted:
        st.warning("질문을 입력해주세요.")

# 대화 히스토리 출력 (최신 대화가 위로 출력되도록 설정)
chat_history_reversed = st.session_state["chat_history"][::-1]  # 대화 히스토리를 역순으로 변경
for speaker, message in chat_history_reversed:
    if speaker == "User":
        st.markdown(f"""
            <div style="background-color:#DCF8C6;padding:10px;border-radius:10px;margin-top:10px;width:80%;margin-left:auto;">
                <p><strong>고객님:</strong> {message}</p>
            </div>
        """, unsafe_allow_html=True)  # 사용자 메시지를 스타일링하여 표시
    else:
        st.markdown(f"""
            <div style="background-color:#F0F0F0;padding:10px;border-radius:10px;margin-top:10px;width:80%;">
                <p><strong>💡 AI 응답:</strong> {message}</p>
            </div>
        """, unsafe_allow_html=True)  # AI 응답을 스타일링하여 표시

# 푸터 추가
st.markdown("""
    <div style="margin-top: 50px; padding: 15px; background-color: #333; color: white; text-align: center; border-radius: 10px;">
        <p>Powered by LangChain & OpenAI API | 🏦 고객의 만족을 위해 언제나 최선을 다합니다.</p>
    </div>
""", unsafe_allow_html=True)  # 페이지 하단에 푸터 표시 (스타일링 적용)