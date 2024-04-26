# Streamlit 前端主程序 多轮 未完成
# Adapted from https://docs.streamlit.io/knowledge-base/tutorials/build-conversational-apps#build-a-simple-chatbot-gui-with-streaming

import streamlit as st
import random
import time

import restllm as client


MODEL = "Qwen-14-4B"

with st.sidebar:
    option = st.selectbox('选择您的模型', (MODEL, 'gemini-pro', 'gemini-pro-vision'))

    if 'model' not in st.session_state or st.session_state.model != option:
        # st.session_state.chat = genai.GenerativeModel(option).start_chat(history=[])
        st.session_state.model = option

    if st.button("清除聊天历史"):
        st.session_state.messages.clear()

    st.write("在此处调整参数：")
    system = st.text_input("系统角色", value="你是一个能干的助手")
    # temperature = st.number_input("温度", min_value=0.0, max_value=1.0, value=0.5, step=0.01)
    # max_token = st.number_input("最大输出 token", min_value=0, value=100)
    # gen_config = genai.types.GenerationConfig(max_output_tokens=max_token, temperature=temperature)

    st.divider()

    upload_image = st.file_uploader("上传图像（视觉模型）", accept_multiple_files=False, type=['jpg', 'png'])

    if upload_image:
        image = Image.open(upload_image)

    st.divider()

    st.markdown("<span ><font size=1>联系我</font></span>", unsafe_allow_html=True)
    "[公众号](<https://mp.weixin.qq.com/s/VCQrnC6mQJUIWDxXGdutag>)"
    "[GitHub](<https://github.com/mcks2000/LLM_Gemini_Pro_Streamlit>)"

def reset_chat():
    st.session_state.messages = []
    st.session_state.context = None

col1, col2 = st.columns([6,1])

with col1:
    st.header(f"Chat with LLM")

with col2:
    st.button('Reset ↺', on_click=reset_chat)


# Initialize chat history
if "messages" not in st.session_state:
    reset_chat()

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("What's up?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        context = st.session_state.context

        msg = client.chat_with_model(MODEL, prompt, system, context=context)
        st.session_state.messages.append({"role": "assistant", "content": msg})
        # st.chat_message("assistant").write(msg)

        # Simulate stream of response with milliseconds delay
        # for chunk, ctx in client.chat_with_model(MODEL, prompt, system, context=context):
        #     full_response += chunk
        #     message_placeholder.markdown(full_response + "▌")
        full_response = msg
        message_placeholder.markdown(full_response)
        # st.session_state.context = ctx

    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": full_response})