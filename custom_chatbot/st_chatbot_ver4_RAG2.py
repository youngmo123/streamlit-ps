import streamlit as st  # Streamlit 라이브러리를 불러옴
from langchain_openai import ChatOpenAI
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.document_loaders import PyPDFLoader
from langchain.chains import ConversationalRetrievalChain
import tempfile

# 페이지 기본 설정
st.set_page_config(
    page_title="커스텀 챗봇 페이지 제목",  # 브라우저 탭에 표시할 페이지 제목
    page_icon="🤖",  # 페이지 탭에 표시할 아이콘
    layout="centered"  # 페이지 레이아웃을 가운데 정렬로 설정
)

# 세션 상태 초기화
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []  # 대화 히스토리용 리스트 초기화

if "memory" not in st.session_state:
    st.session_state["memory"] = []

if 'history' not in st.session_state:
    st.session_state['history'] = []

if 'retriever' not in st.session_state:
    st.session_state['retriever'] = None

if 'recommended_questions' not in st.session_state:
    st.session_state['recommended_questions'] = None

if 'processed_file_name' not in st.session_state:
    st.session_state['processed_file_name'] = None

# 추천 질문 생성 함수 정의
def generate_recommended_questions(text_content):
    llm = ChatOpenAI(
        temperature=0.7,
        model_name='gpt-4o-mini'
    )
    prompt = f"""다음 텍스트를 기반으로, 사용자가 할 만한 추천 질문 5개를 생성해 주세요.

{text_content}

추천 질문:"""
    response = llm.predict(prompt)
    questions = response.strip().split('\n')
    # 질문 목록 정리
    clean_questions = [q.strip('1234567890. ').strip() for q in questions if q.strip()]
    # 최대 5개로 제한
    clean_questions = clean_questions[:5]
    return clean_questions

# 페이지 헤더 설정
st.title("🤖 AI로 무엇이든 물어보세요!")  # 페이지 타이틀 표시
st.markdown("### AI와 함께 궁금증을 해결해 보세요. 아래에 질문을 입력하고 **보내기** 버튼을 눌러보세요!")  # 서브 타이틀 표시

# 응답 다양성 설정 슬라이더 추가 (temperature 조정)
temperature = st.slider("응답 다양성 설정 (Temperature)", 0.0, 1.0, 0.7, step=0.05)

# 대화 스타일 선택 옵션 추가
style = st.selectbox("대화 스타일 선택", ("정중한", "일상적", "전문적"))

# 사이드바에 파일 업로드 기능 추가
uploaded_file = st.sidebar.file_uploader("PDF 파일 업로드", type="pdf")

if uploaded_file:
    # 이전에 처리한 파일과 다른 경우에만 처리
    if st.session_state['processed_file_name'] != uploaded_file.name:
        # 새로운 파일 이름 저장
        st.session_state['processed_file_name'] = uploaded_file.name

        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            tmp_file_path = tmp_file.name

        loader = PyPDFLoader(tmp_file_path)
        data = loader.load()

        embeddings = OpenAIEmbeddings()
        vectors = FAISS.from_documents(data, embeddings)

        # 리트리버를 세션 상태에 저장
        st.session_state['retriever'] = vectors.as_retriever()

        # 문서 내용 추출
        text_content = ""
        char_limit = 5000  # 토큰 제한을 위한 문자 수 제한
        current_chars = 0
        for doc in data:
            page_text = doc.page_content
            if current_chars + len(page_text) > char_limit:
                text_content += page_text[:char_limit - current_chars]
                break
            else:
                text_content += page_text + "\n"
                current_chars += len(page_text)

        # 추천 질문 생성
        recommended_questions = generate_recommended_questions(text_content)
        st.session_state['recommended_questions'] = recommended_questions
    else:
        # 파일이 변경되지 않았으므로 아무 작업도 수행하지 않음
        pass
else:
    # 파일이 업로드되지 않은 경우 세션 상태 초기화
    st.session_state['processed_file_name'] = None
    st.session_state['retriever'] = None
    st.session_state['recommended_questions'] = None

# 사이드바에 추천 질문 표시
if st.session_state['recommended_questions']:
    st.sidebar.markdown("### 추천 질문")
    for idx, question in enumerate(st.session_state['recommended_questions'], 1):
        st.sidebar.write(f"{idx}. {question}")

# ChatOpenAI 모델을 사용하여 답변 생성 및 메모리 추가
def generate_response(input_text): 
    # 대화 스타일에 따라 프롬프트 조정
    style_prefix = {
        "정중한": "정중하게",
        "일상적": "편하게",
        "전문적": "전문적으로"
    }
    style_instruction = style_prefix[style]

    # ChatOpenAI 모델 인스턴스 생성
    llm = ChatOpenAI(
        temperature=temperature,
        model_name='gpt-4o-mini'
    )

    if st.session_state['retriever']:
        # RAG 체인을 사용하여 답변 생성
        chain = ConversationalRetrievalChain.from_llm(
            llm=llm,
            retriever=st.session_state['retriever'],
            return_source_documents=False
        )

        # 대화 히스토리를 입력으로 전달
        result = chain({
            "question": input_text,
            "chat_history": st.session_state['history']
        })
        response = result['answer']

        # 대화 히스토리에 저장
        st.session_state['history'].append((input_text, response))
    else:
        # 메모리를 사용하여 답변 생성
        memory_summary = "\n".join(
            [f"User: {q}\nAI: {a}" for q, a in st.session_state['history']]
        )
        full_input = f"{memory_summary}\n[{style_instruction}] User: {input_text}\nAI:"
        response = llm.predict(full_input)

        # 대화 히스토리에 저장
        st.session_state['history'].append((input_text, response))

    return response  # 응답 반환

# 사용자 입력을 받는 폼 생성 (맨 아래에 입력창 유지)
text = st.text_input("궁금한 점을 입력하세요:", placeholder="예: OpenAI의 텍스트 모델 종류는 어떤 것이 있나요?")
submitted = st.button("보내기")  # '보내기' 버튼 생성하여 제출

# 사용자가 질문을 제출했을 때 답변 생성
if submitted and text:
    response = generate_response(text)  # 응답 생성 함수 호출
    st.session_state["chat_history"].append(("User", text))
    st.session_state["chat_history"].append(("AI", response))

# 대화 히스토리 출력 (입력창 위로 출력되도록 수정)
chat_history_reversed = st.session_state["chat_history"][::-1]
for speaker, message_text in chat_history_reversed:
    if speaker == "User":
        st.write(f"**User:** {message_text}")
    else:
        st.info(f"**AI:** {message_text}")

# 푸터 추가 (선택 사항)
st.markdown("---")
st.caption("Powered by LangChain & OpenAI API")