# Streamlit 底层 LLM主程序 参考 https://github.com/ollama/ollama/blob/main/docs/api.md
import requests
import json
import os

# OLLAMA_HOST = os.environ.get('OLLAMA_HOST', 'http://localhost:11434/api/generate')
# VLLM_HOST = os.environ.get('VLLM_HOST', 'http://localhost:8000/v1/chat/completions')
LOCAL_OLLAMA = "http://localhost:11434"

LOCAL_VLLM = "http://localhost:8000"
REMOTE_VLLM = "https://8000-01hr72c020jtkv3tm9xcnwztye.cloudspaces.litng.ai"

OLLAMA_HOST = os.environ.get('OLLAMA_HOST', LOCAL_OLLAMA + '/api/generate')
VLLM_HOST = os.environ.get('VLLM_HOST', REMOTE_VLLM + '/v1/chat/completions')
BASE_URL = VLLM_HOST

# Ollama: 
def chat(model_name, prompt, system=None, context=None):
    for response, context in generate(model_name, prompt, system=system, context=context):
        print(response, end="", flush=True)
    return context

# Generate a response for a given prompt with a provided model. This is a streaming endpoint, so will be a series of responses.
# The final response object will include statistics and additional data from the request. Use the callback function to override
# the default handler.
def generate(model_name, prompt, system=None, template=None, format="", context=None, options=None, callback=None):
    try:
        url = f"{BASE_URL}"
        payload = {
            "model": model_name, 
            # "prompt": prompt, 
            # "system": system, 
            # "template": template, 
            # "context": context, 
            # "options": options,
            # "format": format,
            "messages": [
                {"role": "system", "content": "你是一个纯文字游戏《沉没之地》的系统旁白，任务是引导用户进行文字游戏的扮演与进行。/n旁白将会：/n1.描述周围场景。例如：酒馆，旅店，被淹旧城镇，怪物，路人，队友 等等。/n2.给用户提供下一步行动的选项，提醒用户做出互动选择，例如：去图书馆查找资料，去酒吧打听消息，去旅店休息，去商店购物，与其他角色沟通组队，选择目的地点等。/n3.天数会随着对话增加，你需要适时的提醒用户当前的天数。用户的目标是在五天内完成任务。如果在五天内没有完成任务，则告诉用户任务失败。如果完成任务则恭喜用户成功通关。/n----/n 故事剧本叫做《沉没之地》，含有神秘的克苏鲁元素，时间背景是在20世纪20年代，用户扮演的是一位落魄的美国私家侦探，收到了一份匿名寄来的神秘的调查委托，要侦探前去一个名为印斯茅斯的岛屿寻找失踪密斯卡托尼克大学考古教授，教授去小岛挖掘古迹已经3个月没有消息了。印斯茅斯正逢雨季，小岛上的城市有一半地区已经被海水淹没，同时与大陆的航线也会中断2个月直到雨季过去，而作为私家侦探的用户，赶上了雨季最后一班上岛的客船，登上了这个小岛。侦探随身携带物品有：一把匕首，装有7颗子弹的小口径手枪，100美元，一卷绷带，还有那封神秘的委托信件。/n----/n 剧情大纲流程为：开始游戏叙述故事背景，登岛，找旅店休息，打听消息，进行调查，前往图书馆，打怪探索，搜寻遗迹等，最终在遗迹中找到失踪的教授。/n----/n 用户输入“游戏开始”后，旁白会以第三人称叙述故事背景、介绍用户扮演的主角情况、主角所处区域，并以有序列表的形式给出三个关于主角可能的下一步行动选项。在用户选择选项后，推进剧情，并在恰当的时候继续给出三个关于主角可能的下一步行动选项。其中一个选项将用户引导到正确的方向，一个将导致用户在当前进度停滞不前，一个将导致用户做无用功甚至倒退（但很隐蔽不易察觉）。"},
                { "role": "user", "content": prompt }
            ],
            "max_tokens": 1024,
            "temperature": 0.7,
            "top_p": 0.9,
            "stream": False
        }
        
        # Remove keys with None values
        payload = {k: v for k, v in payload.items() if v is not None}
        
        with requests.post(url, json=payload, stream=True) as response:
            response.raise_for_status()
            
            # Creating a variable to hold the context history of the final chunk
            final_context = None
            
            # Variable to hold concatenated response strings if no callback is provided
            full_response = ""

            # Iterating over the response line by line and displaying the details
            for line in response.iter_lines():
                if line:
                    # Parsing each line (JSON chunk) and extracting the details
                    chunk = json.loads(line)
                    
                    # If a callback function is provided, call it with the chunk
                    if callback:
                        callback(chunk)
                    else:
                        # If this is not the last chunk, add the "response" field value to full_response and print it
                        if not chunk.get("done"):
                            response_piece = chunk.get("response", "")
                            full_response += response_piece
                            yield response_piece, None

                    # Check if it's the last chunk (done is true)
                    if chunk.get("done"):
                        final_context = chunk.get("context")
            
            # Return the final context
            yield "", final_context
    except requests.exceptions.RequestException as e:
        print("The model hasn't loaded yet. Please retry in a few seconds...")
        # print(f"An error occurred: {e}")
        return None, None

# vLLM: 
def chat_with_model(model, user_input, system=None, context=None):
    # 我们故意抛出一个异常来测试异常处理
    if user_input == "error":
        raise ValueError("Intentional error to test exception handling.")
    # 如果没有异常，返回一个正常的回答

    # 定义请求的 URL
    url = f"{BASE_URL}" # 'http://localhost:8000/v1/chat/completions'
    
    print("\n user_input: " + user_input)

    # 定义请求的数据
    data = {
        "model": model,
        "messages": [
            { "role": "system", "content": system },
            { "role": "user", "content": user_input }
        ],
        "max_tokens": 1024,
        "temperature": 0.7,
        "top_p": 0.9,
        "stream": False # TODO 流式
    }

    # 将数据转换为 JSON 格式
    json_data = json.dumps(data)
    
    print("json_data", json_data)
    print("url", url)

    # 发送 POST 请求
    try: # debug用
        response = requests.post(url, data=json_data, headers={'Content-Type': 'application/json'})
    except requests.ConnectionError as e:
        response.text = {"choices": [{"message": {"content": "1.A; 2.B; 3.C"}}]}

    # 输出响应内容
    response_json = response.text
    print("Response: ", response_json)
    # debug用
    if(response.status_code != 200):
        response_json = json.dumps({"choices": [{"message": {"content": "1.A; 2.B; 3.C"}}]})

    # 解析 JSON 数据
    data = json.loads(response_json)
    # print("json data: ", data)

    # 提取 "message" 中 "role" 为 "assistant" 的 "content"
    assistant_content = data.get("choices", [])[0].get("message", {}).get("content") # data['message']['content']

    # 返回响应内容
    return assistant_content

# TEST 运行streamlit时 需要注释
# user_content = input("Please enter the content for the message: ")
# response_text = send_chat_request("Yi-6", user_content)
# # 打印返回的响应内容
# print(response_text)