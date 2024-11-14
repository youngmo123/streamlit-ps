import streamlit as st  # Streamlit 라이브러리를 불러옴
from langchain_openai import ChatOpenAI
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains import ConversationalRetrievalChain
from langchain.document_loaders import PyPDFLoader
import os
import tempfile

# 페이지 기본 설정
st.set_page_config(
    page_title="AI 기반 고객 응대 서비스",  # 브라우저 탭에 표시할 페이지 제목
    page_icon="🌐",  # 페이지 탭에 표시할 지구본 아이콘
    layout="centered"  # 페이지 레이아웃을 중앙에 정렬하여 모바일 채팅 스타일로 구성
)

# 대화 히스토리 초기화
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []  # 대화 히스토리용 리스트 초기화

if "memory" not in st.session_state:
    st.session_state["memory"] = []

if 'retriever' not in st.session_state:
    # 사전에 정의된 문서 경로 목록
    document_paths = ["Auto_QnA/docs/ma2155_iphone-15-info.pdf", 
                      "Auto_QnA/docs/iPhone 수리 및 서비스 - Apple 지원 (KR).pdf"] # 여기서 경로를 설정하여 백엔드에서 문서를 가져옴
    all_documents = []
    for path in document_paths:
        if os.path.exists(path):
            loader = PyPDFLoader(path)
            data = loader.load()
            all_documents.extend(data)

    embeddings = OpenAIEmbeddings()
    vectors = FAISS.from_documents(all_documents, embeddings)
    st.session_state['retriever'] = vectors.as_retriever()

    # 문서 내용 추출
    text_content = ""
    char_limit = 5000  # 토큰 제한을 위한 문자 수 제한
    current_chars = 0
    for doc in all_documents:
        page_text = doc.page_content
        if current_chars + len(page_text) > char_limit:
            text_content += page_text[:char_limit - current_chars]
            break
        else:
            text_content += page_text + "\n"
            current_chars += len(page_text)

    # 추천 질문 생성
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

    recommended_questions = generate_recommended_questions(text_content)
    st.session_state['recommended_questions'] = recommended_questions

# 상단 헤더 설정
st.markdown("""
    <div style="background-color:#4A90E2;padding:10px;border-radius:10px;">
        <h1 style="color:white;text-align:center;"> 🤖 AI 고객 응답 서비스</h1>
    </div>
""", unsafe_allow_html=True)  # HTML로 상단 헤더 영역의 배경과 색상 스타일링

# 추천 질문 표시 (세션에 저장된 경우에만 표시)
if 'recommended_questions' in st.session_state and st.session_state['recommended_questions']:
    st.markdown("### 추천 질문")
    for idx, question in enumerate(st.session_state['recommended_questions'], 1):
        st.write(f"{idx}. {question}")

# 채팅 스타일의 UI 구성
# ChatOpenAI 모델을 사용하여 답변 생성 및 메모리 추가
def generate_response(input_text): 
    # ChatOpenAI 모델 인스턴스 생성
    llm = ChatOpenAI(
        temperature=1.0,  # 응답의 창의성을 최소화하여 일관성 있는 답변 제공
        model_name='gpt-4o-mini'  # 사전 지정된 AI 모델 사용
    )
    
    if 'retriever' in st.session_state:
        # RAG 체인을 사용하여 답변 생성
        chain = ConversationalRetrievalChain.from_llm(
            llm=llm,
            retriever=st.session_state['retriever'],
            return_source_documents=False
        )
        
        # 대화 히스토리를 입력으로 전달
        result = chain({
            "question": input_text,
            "chat_history": []  # 호출시 새로운 질문으로 가지고 답변 생성
        })
        response = result['answer']
    else:
        # 메모리를 사용하여 답변 생성
        memory_summary = "\n".join(
            [f"User: {q}\nAI: {a}" for q, a in st.session_state['chat_history']]
        )
        full_input = f"{memory_summary}\nUser: {input_text}\nAI:"
        response = llm.predict(full_input)
    
    # 대화 히스토리에 저장
    st.session_state['chat_history'].append(("User", input_text))
    st.session_state['chat_history'].append(("AI", response))
    
    return response  # 응답 반환

# 사용자 입력을 받는 폴 생성
with st.form("question_form"):  # 폴을 생성하여 사용자 질문을 받음
    text = st.text_input(
        "궁금한 점을 입력하세요:", 
        placeholder="예: 아이폰 기능에 대해서 간단하게 설명해주세요.",
    )  # 텍스트 입력 필드 생성
    submitted = st.form_submit_button("보내기", use_container_width=True)  # '보내기' 버튼 생성하여 폴 제출

    # 사용자가 질문을 제출했을 때 답변 생성
    if submitted and text.strip():
        response = generate_response(text)  # 응답 생성 함수 호출
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