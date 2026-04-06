import streamlit as st
from google import genai
from google.genai import types
import os
from dotenv import load_dotenv

# 페이지 설정
st.set_page_config(page_title="전서영 AI", page_icon=":material/face_3:")
st.title(":violet[:material/face_3:] 전서영")
st.caption("전서영이에요.")

MODEL_NAME = "gemini-2.5-flash" # 혹은 사용 중인 모델명

@st.cache_resource
def get_client():
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        st.error("🔑 API 키가 설정되지 않았습니다. .env 파일을 확인해주세요.")
        st.stop()
    return genai.Client(api_key=api_key)

client = get_client()

@st.cache_data
def load_system_prompt(filename):
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            return f.read()
    else:
        st.warning(f"⚠️ {filename} 파일을 찾을 수 없습니다.")
        return ""

# 사이드바에 초기화 버튼 추가 (프롬프트 수정 후 클릭용)
if st.sidebar.button("🔄 대화 및 설정 초기화"):
    for key in st.session_state.keys():
        del st.session_state[key]
    st.rerun()

# 시스템 프롬프트 로드
system_prompt = load_system_prompt('system_prompt.md')

if "chat_session" not in st.session_state:
    st.session_state.chat_session = client.chats.create(
        model=MODEL_NAME,
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
            temperature=0.2, # 값이 낮을수록 지시사항을 더 잘 지킵니다.
        )
    )

# 기존 대화 출력
for content in st.session_state.chat_session.get_history():
    role = 'ai' if content.role == 'model'else 'user'
    with st.chat_message(role):
        for part in content.parts:
            if part.text:
                st.write(part.text)


# 채팅 입력
if prompt := st.chat_input("서영이에게 물어보기"):
    # 유저 메시지 표시 및 저장
    with st.chat_message("user"):
        st.write(prompt)
    

    # AI 응답 생성 및 표시
    with st.chat_message("ai"):

        response = st.session_state.chat_session.send_message(prompt)
        st.write(response.text)
