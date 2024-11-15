import streamlit as st  # Streamlit 라이브러리를 불러옴
from langchain_openai import ChatOpenAI  # LangChain에서 제공하는 ChatOpenAI 모델을 사용하기 위한 모듈
import os  # 운영 체제 관련 모듈 불러옴 (현재 코드에서 사용되지 않음)

# 페이지 기본 설정
st.set_page_config(
    page_title="커스텀 챗봇 페이지 제목",  # 브라우저 탭에 표시할 페이지 제목을 설정
    page_icon="🤖",  # 페이지 탭에 표시할 아이콘을 지정
    layout="centered"  # 페이지 레이아웃을 가운데 정렬로 설정
)

# 대화 히스토리 초기화
if "chat_history" not in st.session_state:  # 세션 상태에 대화 히스토리가 없는 경우
    st.session_state["chat_history"] = []  # 대화 히스토리용 리스트 초기화하여 세션 상태에 추가

# 페이지 헤더 설정
st.title("🤖 AI로 무엇이든 물어보세요!")  # 페이지 상단에 타이틀을 표시
st.markdown("### AI와 함께 궁금증을 해결해 보세요. 아래에 질문을 입력하고 **보내기** 버튼을 눌러보세요!")  # 서브 타이틀과 설명 텍스트 표시

# ChatOpenAI 모델을 사용하여 답변 생성
def generate_response(input_text):  # 사용자 질문에 대한 응답을 생성하는 함수
    llm = ChatOpenAI(  # ChatOpenAI 모델 인스턴스 생성
        temperature=1.0,  # 응답의 창의성을 최소화하여 일관성 있는 답변 제공
        model_name='gpt-4o-mini'  # 사전 지정된 AI 모델 사용
    )
    response = llm.predict(input_text)  # 사용자 입력을 바탕으로 AI 응답 생성
    return response  # 응답 반환

# 사용자 입력을 받는 폼 생성
with st.form("question_form"):  # 폼을 생성하여 사용자 질문을 입력받음
    text = st.text_area("궁금한 점을 입력하세요:", placeholder="예: OpenAI의 텍스트 모델 종류는 어떤 것이 있나요?")  # 질문 입력 텍스트 필드 생성
    submitted = st.form_submit_button("보내기")  # '보내기' 버튼 생성하여 폼 제출

    # 사용자가 질문을 제출했을 때 응답 생성
    if submitted:  # 폼이 제출되었는지 확인
        response = generate_response(text)  # 응답 생성 함수 호출하여 AI 응답 생성
        st.session_state["chat_history"].append(("User", text))  # 사용자 입력을 대화 히스토리에 추가
        st.session_state["chat_history"].append(("AI", response))  # AI 응답을 대화 히스토리에 추가

# 대화 히스토리 출력
for speaker, message in st.session_state["chat_history"]:  # 저장된 대화 히스토리를 반복문으로 출력
    if speaker == "User":  # 화자가 사용자일 경우
        st.write(f"**User:** {message}")  # 사용자의 메시지를 굵게 표시하여 출력
    else:  # 화자가 AI일 경우
        st.info(f"**AI:** {message}")  # AI의 메시지를 정보 박스로 출력

# 푸터 추가 (선택 사항)
st.markdown("---")  # 구분선을 추가하여 페이지 하단을 분리
st.caption("Powered by LangChain & OpenAI API")  # 페이지 하단에 API와 툴 출처 표시