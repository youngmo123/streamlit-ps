import streamlit as st  # Streamlit 라이브러리를 불러옴
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationSummaryMemory

# 페이지 기본 설정
st.set_page_config(
    page_title="커스텀 챗봇 페이지 제목",  # 브라우저 탭에 표시할 페이지 제목
    page_icon="🤖",  # 페이지 탭에 표시할 아이콘
    layout="centered"  # 페이지 레이아웃을 가운데 정렬로 설정
)

# 대화 히스토리 초기화
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []  # 대화 히스토리용 리스트 초기화

# 페이지 헤더 설정
st.title("🤖 AI로 무엇이든 물어보세요!")  # 페이지 타이틀 표시
st.markdown("### AI와 함께 궁금증을 해결해 보세요. 아래에 질문을 입력하고 **보내기** 버튼을 눌러보세요!")  # 서브 타이틀 표시

# 응답 다양성 설정 슬라이더 추가 (temperature 조정)
temperature = st.slider("응답 다양성 설정 (Temperature)", 0.0, 1.0, 0.7, step=0.05)

# 대화 스타일 선택 옵션 추가
style = st.selectbox("대화 스타일 선택", ("정중한", "일상적", "전문적"))

# ChatOpenAI 모델을 사용하여 답변 생성 및 메모리 추가
def generate_response(input_text): 
    # ChatOpenAI 모델 인스턴스 생성
    llm = ChatOpenAI(
        temperature=temperature,  # 사용자가 설정한 응답 다양성 적용
        model_name='gpt-4o-mini'  # 사전 지정된 AI 모델 사용
    )
    
    # ConversationSummaryMemory 설정 (토큰 크기 제한)
    if "memory" not in st.session_state:
        st.session_state["memory"] = ConversationSummaryMemory(llm=llm, max_token_limit=500)  # 최대 500 토큰으로 제한
    
    # 대화 스타일에 따라 프롬프트 조정
    style_prefix = {
        "정중한": "정중하게",
        "일상적": "편하게",
        "전문적": "전문적으로"
    }
    style_instruction = style_prefix[style]
    
    # 대화 히스토리를 메모리에서 가져와 프롬프트에 반영
    memory_summary = st.session_state["memory"].load_memory_variables({})["history"]
    full_input = f"{memory_summary}\n[{style_instruction}] User: {input_text}\nAI:"
    response = llm.predict(full_input)  # 사용자 입력을 바탕으로 AI 응답 생성
    
    # 대화 히스토리를 메모리에 저장
    st.session_state["memory"].save_context({"input": input_text}, {"output": response})
    
    return response  # 응답 반환

# 사용자 입력을 받는 폼 생성 (맨 아래에 입력창 유지)
text = st.text_input("궁금한 점을 입력하세요:", placeholder="예: OpenAI의 텍스트 모델 종류는 어떤 것이 있나요?")  # 텍스트 입력 필드 생성
submitted = st.button("보내기")  # '보내기' 버튼 생성하여 제출

# 사용자가 질문을 제출했을 때 답변 생성
if submitted and text:  # 폼이 제출되었는지 확인하고, 입력이 비어있지 않은지 확인
    response = generate_response(text)  # 응답 생성 함수 호출
    st.session_state["chat_history"].append(("User", text))  # 사용자 입력을 대화 히스토리에 추가
    st.session_state["chat_history"].append(("AI", response))  # AI 응답을 대화 히스토리에 추가

# 대화 히스토리 출력 (입력창 위로 출력되도록 수정)
chat_history_reversed = st.session_state["chat_history"][::-1]  # 대화 히스토리를 역순으로 변경
for speaker, message in chat_history_reversed:
    if speaker == "User":
        st.write(f"**User:** {message}")
    else:
        st.info(f"**AI:** {message}")

# 푸터 추가 (선택 사항)
st.markdown("---")  # 구분선을 추가하여 페이지 하단을 분리
st.caption("Powered by LangChain & OpenAI API")  # 페이지 하단에 API와 툴 출처 표시
