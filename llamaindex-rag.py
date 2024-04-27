from llama_index.core.llms import ChatMessage
from llama_index.llms.openai_like import OpenAILike
from llama_index.llms.vllm import Vllm
import os

# 源码 line 480 /home/zeus/miniconda3/envs/cloudspace/lib/python3.10/site-packages/transformers/tokenization_utils_fast.py
os.environ["HF_HOME"] = "model/"

# 1 使用llamaindex来启动vllm
# 源码 /home/zeus/miniconda3/envs/cloudspace/lib/python3.10/site-packages/llama_index/llms/vllm/base.py
# llm = Vllm(
#     model="model/Alibaba/Qwen1.5-14B-Chat-AWQ", # 本地或HF模型
#     tensor_parallel_size=1,
#     max_new_tokens=100,
#     vllm_kwargs={"max_model_len": 256, "enforce_eager": True},
# )
# chat_history = [  
#     ChatMessage(role="system", content="You are a bartender.I often like to order banana juice."),  
#     ChatMessage(role="user", content="What do I enjoy drinking?"),  
# ]  
# output = llm.chat(chat_history)  
# print(output)

# 2 使用已启动的vllm服务 USE: Start vLLM first
# 源码 /home/zeus/miniconda3/envs/cloudspace/lib/python3.10/site-packages/llama_index/llms/openai/base.py
llm = OpenAILike(
    model="Qwen-14-4B",
    # api_base="http://localhost:8000/v1/",
    api_base="https://8000-01hr72c020jtkv3tm9xcnwztye.cloudspaces.litng.ai/v1/",
    timeout=60,  # secs
    api_key="loremIpsum",
    is_chat_model=True,
    context_window=32768,
)
chat_history = [
    # ChatMessage(role="system", content="You are a bartender.I often like to order banana juice."),
    # ChatMessage(role="user", content="What do I enjoy drinking?"),
    ChatMessage(role="system", content="你是一个纯文字游戏《沉没之地》的系统旁白，任务是引导用户进行文字游戏的扮演与进行。/n旁白将会：/n1.描述周围场景。例如：酒馆，旅店，被淹旧城镇，怪物，路人，队友 等等。/n2.给用户提供下一步行动的选项，提醒用户做出互动选择，例如：去图书馆查找资料，去酒吧打听消息，去旅店休息，去商店购物，与其他角色沟通组队，选择目的地点等。/n3.天数会随着对话增加，你需要适时的提醒用户当前的天数。用户的目标是在五天内完成任务。如果在五天内没有完成任务，则告诉用户任务失败。如果完成任务则恭喜用户成功通关。/n----/n 故事剧本叫做《沉没之地》，含有神秘的克苏鲁元素，时间背景是在20世纪20年代，用户扮演的是一位落魄的美国私家侦探，收到了一份匿名寄来的神秘的调查委托，要侦探前去一个名为印斯茅斯的岛屿寻找失踪密斯卡托尼克大学考古教授，教授去小岛挖掘古迹已经3个月没有消息了。印斯茅斯正逢雨季，小岛上的城市有一半地区已经被海水淹没，同时与大陆的航线也会中断2个月直到雨季过去，而作为私家侦探的用户，赶上了雨季最后一班上岛的客船，登上了这个小岛。侦探随身携带物品有：一把匕首，装有7颗子弹的小口径手枪，100美元，一卷绷带，还有那封神秘的委托信件。/n----/n 剧情大纲流程为：开始游戏叙述故事背景，登岛，找旅店休息，打听消息，进行调查，前往图书馆，打怪探索，搜寻遗迹等，最终在遗迹中找到失踪的教授。/n----/n 用户输入“游戏开始”后，旁白会以第三人称叙述故事背景、介绍用户扮演的主角情况、主角所处区域，并以有序列表的形式给出三个关于主角可能的下一步行动选项。在用户选择选项后，推进剧情，并在恰当的时候继续给出三个关于主角可能的下一步行动选项。其中一个选项将用户引导到正确的方向，一个将导致用户在当前进度停滞不前，一个将导致用户做无用功甚至倒退（但很隐蔽不易察觉）。"),
    ChatMessage(role="user", content="开始游戏"),
]
output = llm.chat(chat_history)
print(output)


from llama_index.core import Settings, SimpleDirectoryReader, VectorStoreIndex
Settings.llm = llm # Ollama(model="llama2", request_timeout=120.0)
# 在主机上
# Settings.embed_model = "local" # HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")
# TODO 在客户端上 需要下载HuggingFaceEmbedding
Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")
Settings.num_output = 512
Settings.context_window = 4096
documents = SimpleDirectoryReader(
    input_dir="data/llama_index/documents",
).load_data()
index = VectorStoreIndex.from_documents(
    documents=documents,
)
engine = index.as_query_engine(llm=llm)
output = engine.query("What do I like to drink?")
print("query answer: ", output)

# TODO 完善多伦对话
# Everything from above, till and including the creation of the index.
engine = index.as_chat_engine()
output = engine.chat("What do I like to drink?") # "What is the game about?"
print("as_chat_engine output: ", output) # "You enjoy drinking coffee."

output = engine.chat("How do I make it myself?") # "How to start the game?"
print("as_chat_engine output: ", output) # "You brew coffee with a Aeropress."

# debug
# ValueError: Could not extract tool use from input text: Thought: 用户选择了先找旅店休息，我将模拟这个场景。
# Action: story_teller