from llama_index.core.llms import ChatMessage
from llama_index.llms.openai_like import OpenAILike
from llama_index.llms.vllm import Vllm
import os

# 源码 line 480 /home/zeus/miniconda3/envs/cloudspace/lib/python3.10/site-packages/transformers/tokenization_utils_fast.py
os.environ["HF_HOME"] = "model/"

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

# 源码 /home/zeus/miniconda3/envs/cloudspace/lib/python3.10/site-packages/llama_index/llms/openai/base.py
llm = OpenAILike(
    model="Qwen-14-4B",
    api_base="http://localhost:8000/v1/",
    timeout=60,  # secs
    api_key="loremIpsum",
    is_chat_model=True,
    context_window=32768,
)
chat_history = [
    ChatMessage(role="system", content="You are a bartender.I often like to order banana juice."),
    ChatMessage(role="user", content="What do I enjoy drinking?"),
]
output = llm.chat(chat_history)
print(output)



from llama_index.core import Settings, SimpleDirectoryReader, VectorStoreIndex
Settings.llm = llm # Ollama(model="llama2", request_timeout=120.0)
Settings.embed_model = "local" # HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")
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
print("engine output: ", output)


# Everything from above, till and including the creation of the index.
engine = index.as_chat_engine()
output = engine.chat("What do I like to drink?")
print(output) # "You enjoy drinking coffee."
output = engine.chat("How do I make it myself?")
print(output) # "You brew coffee with a Aeropress."