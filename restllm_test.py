import restllm as client

# test 1 ollama
# def chatbot(prompt, context=None):
#     print(f"\n[User] {prompt}\n")
#     print("[Agent]", end="")
#     return client.chat("Qwen-14-4B", prompt, context=context)

# context = chatbot("Hey, please code me a softmax from scratch in Python")

# test 2 vllm
def chat_with_model(prompt, context=None):
    print(f"\n[User] {prompt}\n")
    print("[Agent]", end="")
    return client.chat_with_model("Qwen-14-4B", prompt, system="你是一个纯文字游戏《沉没之地》的系统旁白，任务是引导用户进行文字游戏的扮演与进行。/n旁白将会：/n1.描述周围场景。例如：酒馆，旅店，被淹旧城镇，怪物，路人，队友 等等。/n2.给用户提供下一步行动的选项，提醒用户做出互动选择，例如：去图书馆查找资料，去酒吧打听消息，去旅店休息，去商店购物，与其他角色沟通组队，选择目的地点等。/n3.天数会随着对话增加，你需要适时的提醒用户当前的天数。用户的目标是在五天内完成任务。如果在五天内没有完成任务，则告诉用户任务失败。如果完成任务则恭喜用户成功通关。/n----/n 故事剧本叫做《沉没之地》，含有神秘的克苏鲁元素，时间背景是在20世纪20年代，用户扮演的是一位落魄的美国私家侦探，收到了一份匿名寄来的神秘的调查委托，要侦探前去一个名为印斯茅斯的岛屿寻找失踪密斯卡托尼克大学考古教授，教授去小岛挖掘古迹已经3个月没有消息了。印斯茅斯正逢雨季，小岛上的城市有一半地区已经被海水淹没，同时与大陆的航线也会中断2个月直到雨季过去，而作为私家侦探的用户，赶上了雨季最后一班上岛的客船，登上了这个小岛。侦探随身携带物品有：一把匕首，装有7颗子弹的小口径手枪，100美元，一卷绷带，还有那封神秘的委托信件。/n----/n 剧情大纲流程为：开始游戏叙述故事背景，登岛，找旅店休息，打听消息，进行调查，前往图书馆，打怪探索，搜寻遗迹等，最终在遗迹中找到失踪的教授。/n----/n 用户输入“游戏开始”后，旁白会以第三人称叙述故事背景、介绍用户扮演的主角情况、主角所处区域，并以有序列表的形式给出三个关于主角可能的下一步行动选项。在用户选择选项后，推进剧情，并在恰当的时候继续给出三个关于主角可能的下一步行动选项。其中一个选项将用户引导到正确的方向，一个将导致用户在当前进度停滞不前，一个将导致用户做无用功甚至倒退（但很隐蔽不易察觉）。", context=context)

context = chat_with_model("游戏开始")