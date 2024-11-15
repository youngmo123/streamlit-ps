import streamlit as st
import whisper

# Whisper 모델 로드 함수
# Whisper 모델은 OpenAI의 음성 인식 모델로, 음성을 텍스트로 변환합니다.
@st.cache_resource
def load_whisper_model():
    return whisper.load_model("base")  # Whisper 모델의 "base" 버전 로드

# Whisper 모델 초기화
whisper_model = load_whisper_model()

# Streamlit UI 시작
st.title("음성 회의록 변환 서비스")  # 앱의 제목 설정
st.write("음성 파일을 업로드하고 텍스트로 변환된 내용을 확인하세요!")  # 간단한 설명 제공

# 파일 업로드 컴포넌트 (MP3, WAV, M4A 형식 지원)
uploaded_file = st.file_uploader("음성 파일 업로드 (MP3, WAV, M4A)", type=["mp3", "wav", "m4a"])

# 파일이 업로드되었는지 확인
if uploaded_file:
    # 음성 파일 처리 진행 메시지 표시
    with st.spinner("음성을 텍스트로 변환 중..."):
        try:
            # 업로드된 파일을 임시 저장
            audio_path = f"temp_audio.{uploaded_file.name.split('.')[-1]}"  # 파일 확장자 유지
            with open(audio_path, "wb") as f:
                f.write(uploaded_file.read())  # 파일 내용을 저장

            # Whisper 모델을 사용하여 음성을 텍스트로 변환
            result = whisper_model.transcribe(audio_path)
            text = result["text"]  # 변환된 텍스트 추출
            st.success("음성 텍스트 변환 완료!")  # 성공 메시지 출력
        except Exception as e:
            # 오류 발생 시 오류 메시지 출력
            st.error(f"음성 변환 실패: {e}")
            text = ""  # 텍스트 변환 실패 시 빈 값으로 설정

    # 변환된 텍스트가 있을 경우
    if text:
        # 변환된 텍스트를 표시
        st.subheader("변환된 텍스트")  # 텍스트 표시 섹션 제목
        with st.expander("전체 텍스트 보기"):  # 사용자가 텍스트를 확장하여 볼 수 있도록 구성
            st.text_area("텍스트", text, height=300)  # 텍스트 표시 영역
    else:
        # 텍스트 변환 실패 시 경고 메시지 출력
        st.warning("음성 파일을 처리하는 중 문제가 발생했습니다. 올바른 파일을 업로드했는지 확인하세요.")
