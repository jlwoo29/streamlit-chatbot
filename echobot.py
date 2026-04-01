import streamlit as st

st.title(":orange[:material/smart_toy:] 에코봇")

st.caption("내 말을 따라하는 따라쟁이입니다.")

if "messages" not in st.session_state:
    st.session_state.messages = []


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])


if prompt := st.chat_input("따라쟁이에게 물어보기"):
    with st.chat_message("user"):
        st.write(prompt)
        message = {
            "role": "user",
            "content": prompt
        }
        st.session_state.messages.append(message)

    with st.chat_message("ai"):
        st.write(prompt)
        message = {
            "role": "ai",
            "content": prompt
        }
        st.session_state.messages.append(message)

