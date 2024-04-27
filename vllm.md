# REF
https://docs.vllm.ai/en/stable/getting_started/examples/gradio_webserver.html
https://bdtechtalks.com/2023/08/14/llm-api-server-nocode/
https://blog.csdn.net/weixin_43278082/article/details/134944579
https://blog.csdn.net/arkohut/article/details/135274973


# 安装
安装vllm
pip install vllm

安装 Flash-Attention
pip install flash-attn --no-build-isolation --use-pep517

导出依赖
pip freeze > req.txt

安装依赖
pip install -r req.txt


# 启动
## 方式1 直接启动后端
python cli_demo.py --model_path /teamspace/studios/this_studio/model/Llama/Llama3-Chinese
## 方式1 启动web前端
python web_demo.py --model_path /teamspace/studios/this_studio/model/Llama/Llama3-Chinese

## 方式2 vllm Offline Inference CLI本地推理
https://docs.vllm.ai/en/stable/getting_started/examples/offline_inference.html
见文件 /teamspace/studios/this_studio/github/llama3-chinese/vllm_local.py
主要API llm = LLM(model="...")

## 方式3 vllm 前后端分离 compatibility with the OpenAI API的在线推理
### 环境优化
export PYTORCH_CUDA_ALLOC_CONF=max_split_size_mb:64
### 启动模型
可用 千问
`python -m vllm.entrypoints.openai.api_server --served-model-name Qwen-14-4B --model /teamspace/studios/this_studio/model/Alibaba/Qwen1.5-14B-Chat-AWQ -q awq --max-model-len 2048 --enforce-eager --trust-remote-code`
可用 llama3
`python -m vllm.entrypoints.openai.api_server --served-model-name Llama3-Chinese-8B --model /teamspace/studios/this_studio/model/Llama/Llama3-Chinese`
不可用
- python -m vllm.entrypoints.openai.api_server --served-model-name Mistral --model /teamspace/studios/this_studio/model/Mistral/Mistral-7B-Instruct-v0.2
不可用 格式问题
- python -m vllm.entrypoints.openai.api_server --served-model-name internlm2 --model /teamspace/studios/this_studio/model/Shanghai/internlm2-chat-7b
可用 零一
`python -m vllm.entrypoints.openai.api_server --served-model-name Yi-6 --model /teamspace/studios/this_studio/model/ZeroOne/Yi-6B-Chat-4bits --max-model-len 2048 -q awq --enforce-eager`
`python -m vllm.entrypoints.openai.api_server --served-model-name Yi-34 --model /teamspace/studios/this_studio/model/ZeroOne/Yi-34B-Chat-4bits --max-model-len 2048 -q awq --enforce-eager`
### 测试后端 注意model名称对应
- 本地
curl http://localhost:8000/v1/completions \
-H "Content-Type: application/json" \
-d '{
    "model": "Qwen-14-4B",
    "prompt": "给我的黑马起个名字：",
    "max_tokens": 5,
    "temperature": 0.5
}'
- 远程
curl https://8000-01hr72c020jtkv3tm9xcnwztye.cloudspaces.litng.ai/v1/chat/completions \
-H "Content-Type: application/json" \
-d '{
    "model": "Yi-34",
    "messages": [
        {"role": "system", "content": "你是一个能干的助手."},
        {"role": "user", "content": "谁赢得了2020年的世界职业棒球大赛?"},
        {"role": "assistant", "content": "洛杉矶道奇队在2020年赢得了世界职业棒球大赛冠军."},
        {"role": "user", "content": "它在哪里举办的?"}
    ],
    "max_tokens": 1024,
    "temperature": 0.2
}'
### 3.1 前端方式1：Gradio Webserver
https://docs.vllm.ai/en/stable/getting_started/examples/gradio_webserver.html
文件 python vllm_gradio_demo.py
主要使用 python原生的requests.post 以及 gr.Textbox
### 3.2 前端方式2：Gradio OpenAI Chatbot Webserver
https://docs.vllm.ai/en/stable/getting_started/examples/gradio_openai_chatbot_webserver.html
文件 python vllm_web_demo.py --model Llama3-Chinese
主要API gr.ChatInterface


# benchmark
python /teamspace/studios/this_studio/github/vllm/benchmarks/benchmark_throughput.py \
    --backend vllm \
    --input-len 128 --output-len 512 \
    --model /teamspace/studios/this_studio/model/Llama/Llama3-Chinese \
    <!-- -q awq \ -->
    --num-prompts 100 --seed 1100 \
    --trust-remote-code \
    --max-model-len 2048

