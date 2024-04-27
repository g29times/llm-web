# Streamlit 前端主程序 多轮 未完成
# Adapted from https://docs.streamlit.io/knowledge-base/tutorials/build-conversational-apps#build-a-simple-chatbot-gui-with-streaming

# TODO
# 1. 修复多轮对话
# 2. 第一次对话会输出两次

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
    # TODO 提供一些可选项
    system = st.selectbox("系统角色", ("你是一个能干的助手", 
                                   '你是一个纯文字游戏《沉没之地》的系统旁白，任务是引导用户进行文字游戏的扮演与进行。/n旁白将会：/n1.描述周围场景。例如：酒馆，旅店，被淹旧城镇，怪物，路人，队友 等等。/n2.给用户提供下一步行动的选项，提醒用户做出互动选择，例如：去图书馆查找资料，去酒吧打听消息，去旅店休息，去商店购物，与其他角色沟通组队，选择目的地点等。/n3.天数会随着对话增加，你需要适时的提醒用户当前的天数。用户的目标是在五天内完成任务。如果在五天内没有完成任务，则告诉用户任务失败。如果完成任务则恭喜用户成功通关。/n----/n 故事剧本叫做《沉没之地》，含有神秘的克苏鲁元素，时间背景是在20世纪20年代，用户扮演的是一位落魄的美国私家侦探，收到了一份匿名寄来的神秘的调查委托，要侦探前去一个名为印斯茅斯的岛屿寻找失踪密斯卡托尼克大学考古教授，教授去小岛挖掘古迹已经3个月没有消息了。印斯茅斯正逢雨季，小岛上的城市有一半地区已经被海水淹没，同时与大陆的航线也会中断2个月直到雨季过去，而作为私家侦探的用户，赶上了雨季最后一班上岛的客船，登上了这个小岛。侦探随身携带物品有：一把匕首，装有7颗子弹的小口径手枪，100美元，一卷绷带，还有那封神秘的委托信件。/n----/n 剧情大纲流程为：开始游戏叙述故事背景，登岛，找旅店休息，打听消息，进行调查，前往图书馆，打怪探索，搜寻遗迹等，最终在遗迹中找到失踪的教授。/n----/n 用户输入“游戏开始”后，旁白会以第三人称叙述故事背景、介绍用户扮演的主角情况、主角所处区域，并以有序列表的形式给出三个关于主角可能的下一步行动选项。在用户选择选项后，推进剧情，并在恰当的时候继续给出三个关于主角可能的下一步行动选项。其中一个选项将用户引导到正确的方向，一个将导致用户在当前进度停滞不前，一个将导致用户做无用功甚至倒退（但很隐蔽不易察觉）。'
                                   ))
    # system = st.text_input("系统角色", value="你是一个能干的助手")
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
prompt = st.chat_input("What's up?")
if prompt:
# if prompt := st.chat_input("What's up?"):
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

        print("system ----------------- ", system)
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