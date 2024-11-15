# 기본 템플릿 제작
import streamlit as st  # Streamlit 라이브러리를 불러옴
from langchain_openai import ChatOpenAI
# 페이지 기본 설정
st.set_page_config(
    page_title="커스텀 챗봇 페이지 제목",  # 브라우저 탭에 표시할 페이지 제목
    page_icon="🤖",  # 페이지 탭에 표시할 아이콘
    layout="centered"  # 페이지 레이아웃을 가운데 정렬로 설정
)

# 페이지 헤더 설정
st.title("🤖 AI로 무엇이든 물어보세요!")  # 페이지 타이틀 표시
st.markdown("### AI와 함께 궁금증을 해결해 보세요. 아래에 질문을 입력하고 **보내기** 버튼을 눌러보세요!")  # 서브 타이틀 표시

# ChatOpenAI 모델을 사용하여 답변 생성
def generate_response(input_text): 
    # ChatOpenAI 모델 인스턴스 생성
    llm = ChatOpenAI(
        temperature=1.0,  # 응답의 창의성을 최소화하여 일관성 있는 답변 제공
        model_name='gpt-4o-mini'  # 사전 지정된 AI 모델 사용
    )
    response = llm.predict(input_text)  # 사용자 입력을 바탕으로 AI 응답 생성
    st.info(response)  # 생성된 답변을 스트림릿의 info 컴포넌트로 표시

# 사용자 입력을 받는 폼 생성
with st.form("question_form"):  # 폼을 생성하여 사용자 질문을 받음
    text = st.text_area("궁금한 점을 입력하세요:", placeholder="예: OpenAI의 텍스트 모델 종류는 어떤 것이 있나요?")  # 텍스트 입력 필드 생성
    submitted = st.form_submit_button("보내기")  # '보내기' 버튼 생성하여 폼 제출

    # 사용자가 질문을 제출했을 때 답변 생성
    if submitted:  # 폼이 제출되었는지 확인
        generate_response(text)  # 사용자의 입력 텍스트로 응답 생성 함수 호출

# 푸터 추가 (선택 사항)
st.markdown("---")  # 구분선을 추가하여 페이지 하단을 분리
st.caption("Powered by LangChain & OpenAI API")  # 페이지 하단에 API와 툴 출처 표시