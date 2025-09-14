from openai import OpenAI
import httpx
# client = OpenAI(
#             base_url="http://localhost:11434/v1",  # 注意/v1后缀
#             api_key="ollama", # 任意非空字符串即可
#             max_retries=3,
#         )

# response =  client.chat.completions.create(
#             model="qwen2.5vl:7b",  # 或 gpt-4-turbo
#             messages=[
#                 {"role":"user", "content": "'/home/wwk/workspace/ai_project/cyberHat/agent/uploads/images/k210_camera_1757686834_None.png' 这张图片里面有什么东西， 请根据图片信息进行回答"}
#             ],
#             timeout=120
# )
# print(response.choices[0].message.content)

# OLLAMA_CHAT_MODEL="qwen2.5vl:7b"
# OLLAMA_BASE_URL="http://localhost:11434"
# with httpx.Client() as client:
#     response =  client.post(
#                 f"{OLLAMA_BASE_URL}/api/generate",
#                 json={
#                     "model": OLLAMA_CHAT_MODEL,
#                     "prompt": "'/home/wwk/workspace/ai_project/cyberHat/agent/uploads/images/k210_camera_1757686834_None.png' 这张图片里面有什么东西， 请根据图片信息进行回答",
#                     "stream": False  # 非流式响应
#                 },
#                 timeout=60.0
#         )
#     response.raise_for_status()
#     result = response.json()
#     print(OLLAMA_CHAT_MODEL +" Result: " + str(result['response']))





import base64
import requests
import json

import os

class LLMAgent():
    def __init__(self):
        # 配置参数
        self.image_path = "/home/wwk/workspace/ai_project/cyberHat/agent/uploads/images/k210_camera_1757688672_person.png"  # 替换为您的图片路径
        self.base_url = "http://localhost:11434/v1"  # Ollama的OpenAI兼容端点
        self.api_key = "ollama"  # Ollama通常不需要认证，但有些版本需要任意值

        pass

    def encode_image_to_base64(self, image_path):
        """将图片转换为Base64编码"""
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    def chat(self, message, images=[]):
        try:
            
            # 构建请求头
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}"  # 对于本地Ollama，这通常不是必须的
            }
            # 发送请求
            payload = self.gen_request(message, images)
            print("payload: ", payload)
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=payload ,
                timeout=60  # 超时时间设长一些，因为处理图片需要时间
            )
            
            # 检查响应

            if response.status_code == 200:
                result = response.json()
                answer = result['choices'][0]['message']['content']
                print("✅ 识别结果：")
                print(answer)
                print(f"\n📊 使用token数: {result['usage']['total_tokens']}")
                return answer
            else:
                print(f"❌ 请求失败: {response.status_code}")
                print("错误信息:", response.text)
                return response.text

        except requests.exceptions.RequestException as e:
            print(f"❌ 网络请求错误: {e}")
            return response.text

        except KeyError as e:
            print(f"❌ 解析响应出错: {e}")
            print("原始响应:", response.text)
            return response.text

        except Exception as e:
            print(f"❌ 发生未知错误: {e}")
            return ""

    def gen_request(self, message="", images=[]):
        if not message:
            message ="请详细描述这张图片的内容。图片中有什么物体、人物、文字或场景？"
        message_ls = []
        message_ls.append({"type": "text","text":  message}) 
        for image_path in images:
            # 编码图片
            print("image_path=  ", image_path)
            req = {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{self.encode_image_to_base64(image_path)}"
                    }
            }
            message_ls.append(req)

        

        # 构建请求数据 - 这是关键部分！
        payload = {
            "model": "qwen2.5vl:7b",  # Ollama中的模型名称
            "messages": [
                {
                    "role": "user",
                    "content": message_ls
                }
            ],
            # "max_tokens": 1024,
            "stream": False  # 设置为True可以流式输出
        }
        return payload


client = LLMAgent()
image_root = "/home/wwk/workspace/ai_project/cyberHat/agent/uploads/images/"
image_files = ["k210_camera_1757688975_person.png","k210_camera_1757688982_person.png"]
images = [ os.path.join(image_root, i) for i in image_files]
ret = client.chat("请详细描述这一张或多张图片的内容。图片中有什么物体、人物、文字或场景？",images)


# import base64
# import requests
# import json

# def encode_image_to_base64(image_path):
#     """将图片转换为Base64编码"""
#     with open(image_path, "rb") as image_file:
#         return base64.b64encode(image_file.read()).decode('utf-8')

# # 配置参数
# image_path = "/home/wwk/workspace/ai_project/cyberHat/agent/uploads/images/k210_camera_1757688975_person.png"  # 替换为您的图片路径
# base_url = "http://localhost:11434/v1"  # Ollama的OpenAI兼容端点
# api_key = "ollama"  # Ollama通常不需要认证，但有些版本需要任意值

# # 编码图片
# base64_image = encode_image_to_base64(image_path)

# # 构建请求头
# headers = {
#     "Content-Type": "application/json",
#     "Authorization": f"Bearer {api_key}"  # 对于本地Ollama，这通常不是必须的
# }

# # 构建请求数据 - 这是关键部分！
# payload = {
#     "model": "qwen2.5vl:7b",  # Ollama中的模型名称
#     "messages": [
#         {
#             "role": "user",
#             "content": [
#                 {
#                     "type": "text",
#                     "text": "请详细描述这张图片的内容。图片中有什么物体、人物、文字或场景？"
#                 },
#                 {
#                     "type": "image_url",
#                     "image_url": {
#                         "url": f"data:image/jpeg;base64,{base64_image}"
#                     }
#                 }
#             ]
#         }
#     ],
#     "max_tokens": 1024,
#     "stream": False  # 设置为True可以流式输出
# }

# try:
#     # 发送请求
#     response = requests.post(
#         f"{base_url}/chat/completions",
#         headers=headers,
#         json=payload,
#         timeout=60  # 超时时间设长一些，因为处理图片需要时间
#     )
    
#     # 检查响应
#     if response.status_code == 200:
#         result = response.json()
#         answer = result['choices'][0]['message']['content']
#         print("✅ 识别结果：")
#         print(answer)
#         print(f"\n📊 使用token数: {result['usage']['total_tokens']}")
#     else:
#         print(f"❌ 请求失败: {response.status_code}")
#         print("错误信息:", response.text)

# except requests.exceptions.RequestException as e:
#     print(f"❌ 网络请求错误: {e}")
# except KeyError as e:
#     print(f"❌ 解析响应出错: {e}")
#     print("原始响应:", response.text)
# except Exception as e:
#     print(f"❌ 发生未知错误: {e}")