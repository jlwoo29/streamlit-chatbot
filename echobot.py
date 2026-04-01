import streamlit as st

st.title(":red[:material/smart_toy:] 에코봇")

if prompt :st.chat_input('에코봇에게 물어보기'):

    with st.chat_message('user'):
        st.write(prompt)

    with st.chat_message('ai'):
        st.write(prompt)
