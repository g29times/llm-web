# Streamlit 前端主程序 单轮 完成
# streamlit run --server.port 8501 web/streamlit.py
# https://streamlit.io/gallery?category=llms
# https://github.com/dataprofessor/llama2/blob/master/streamlit_app.py
# https://github.com/streamlit/llm-examples/blob/main/Chatbot.py

# from openai import OpenAI
import streamlit as st
import restllm

# with st.sidebar:
#     openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
#     "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"
#     "[View the source code](https://github.com/streamlit/llm-examples/blob/main/Chatbot.py)"
#     "[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/streamlit/llm-examples?quickstart=1)"

st.title("🍄 Hello vLLM 🍁")
st.caption("🚀❤️ Let's start adventure!")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "💬 Hi! 准备好游戏了吗? 你可以说：游戏开始"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    # if not openai_api_key:
    #     st.info("Please add your OpenAI API key to continue.")
    #     st.stop()

    # client = OpenAI(api_key=openai_api_key)
    # message记录到session里
    st.session_state.messages.append({"role": "user", "content": prompt})
    # 显示到UI对话框
    st.chat_message("user").write(prompt)
    
    # if st.session_state.messages[-1]["role"] != "assistant":

    # response = client.chat.completions.create(model="gpt-3.5-turbo", messages=st.session_state.messages)
    # msg = response.choices[0].message.content
    # st.info(prompt)
    try:
        msg = restllm.chat_with_model('Qwen-14-4B', prompt)
        st.session_state.messages.append({"role": "assistant", "content": msg})
        st.chat_message("assistant").write(msg)
    except ConnectionError as e:
        # 这里可以添加日志记录或其他异常处理代码
        st.session_state.messages.append({"role": "assistant", 
            "content": "I'm sorry, I'm unable to connect to the server."})
        st.chat_message("assistant").write("I'm sorry, I'm unable to connect to the server.")
    except Exception as e:
            # traceback.print_exc()
        st.chat_message("assistant").write(e)