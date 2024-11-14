import os
import tempfile
from pydub import AudioSegment
import streamlit as st
import whisper

@st.cache_resource
def load_whisper_model():
    # Whisper 모델을 불러오는 함수. Streamlit에서 캐싱하여 성능 향상.
    return whisper.load_model("small")

whisper_model = load_whisper_model()  # Whisper 모델 로드

st.title("음성 회의록 변환 서비스")  # 서비스 제목
st.write("음성 파일을 업로드하고 텍스트로 변환된 내용을 확인하세요!")  # 간단한 설명

MAX_FILE_SIZE_MB = 100  # 업로드 가능한 최대 파일 크기 (100MB)
uploaded_file = st.file_uploader(
    "음성 파일 업로드 (MP3, WAV, M4A, 최대 100MB)", type=["mp3", "wav", "m4a"]
)  # 사용자로부터 파일 업로드 받기

if uploaded_file:  # 파일이 업로드된 경우
    if uploaded_file.size > MAX_FILE_SIZE_MB * 1024 * 1024:
        # 파일 크기가 너무 큰 경우 에러 메시지 출력
        st.error("파일 크기가 너무 큽니다. 최대 100MB 이하의 파일만 업로드해주세요.")
    else:
        temp_audio_path = None  # 임시 파일 경로 초기화
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
                if uploaded_file.name.split(".")[-1] != "wav":
                    # 파일이 WAV 형식이 아닌 경우, WAV로 변환
                    audio = AudioSegment.from_file(uploaded_file)
                    audio.export(temp_audio.name, format="wav")
                else:
                    # 파일이 WAV 형식인 경우 그대로 저장
                    temp_audio.write(uploaded_file.read())
                temp_audio_path = temp_audio.name  # 임시 경로 저장

            result = whisper_model.transcribe(temp_audio_path)  # 음성 파일을 텍스트로 변환
            text = result["text"]  # 변환된 텍스트 가져오기

            st.success("음성 텍스트 변환 완료!")  # 성공 메시지 출력
            st.subheader("변환된 텍스트")  # 결과 섹션 제목
            with st.expander("전체 텍스트 보기"):
                # 변환된 텍스트를 텍스트 에어리어로 표시
                st.text_area("텍스트", text, height=500)

        except Exception as e:
            # 변환 실패 시 에러 메시지 출력
            st.error(f"음성 변환 실패: {e}")

        finally:
            # 임시 파일이 존재하면 삭제
            if temp_audio_path and os.path.exists(temp_audio_path):
                os.remove(temp_audio_path)