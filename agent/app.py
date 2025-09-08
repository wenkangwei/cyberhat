# from cgi import test
import collections
from urllib import request
# from heapq import merge
# from pickle import NONE
# from BookMonster.agent.app import gb_state
import httpx  # 替代requests，支持异步
# from memory.client.memory import MemoryClient
from common.context import Context
import hashlib

# import re
from fastapi import FastAPI, UploadFile, File, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from datetime import datetime
import logging

from dis import Instruction
from pydantic import BaseModel, Field, validator
from typing import List, Literal, Optional
import base64
import os
from fastapi import FastAPI, UploadFile, File, HTTPException
import json
import random
import threading
import time
# from agent import *
import asyncio
from constant import *
from tools.utils import *
# # Debug

from tools.webpage_crawler import webpage_crawler
from pyngrok import ngrok




from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import JSONResponse
from typing import List, Optional
import uvicorn
import os
import uuid
from datetime import datetime
import shutil
from pathlib import Path

# 使用 ngrok 连接指定端口，获取公共 URL
# 这里假设你已经按照前面的方法设置了 NGROK_AUTH_TOKEN（推荐）
# 如果没有，以下代码仍会运行，但每次连接的 URL 都会变化且有限制
port = 8000
# front_end_port=3000
# public_url = ngrok.connect(port, bind_tls=True).public_url
public_url="http://localhost:8000"
print(f" * Public URL: {public_url}")



tmp_data={"maxHp":"10","skill":[{"question":["202304010001","pikaqiu的属性是什么？",1],"answer1":"雷属性","answer2":"高铁属性","answer3":"水属性","correct_answer":"雷属性"},{"question":["202304010002","pikaqiu喜欢看的书籍是什么？",2],"answer1":"钢铁就是力量","answer2":"钢铁是怎样炼成的","answer3":"钢铁的未来","correct_answer":"钢铁就是力量"},{"question":["202304010003","pikaqiu的主人叫什么名字？",3],"answer1":"小k","answer2":"小明","answer3":"小红","correct_answer":"小k"},{"question":["202304010004","pikaqiu的主人是做什么的？",4],"answer1":"算法工程师","answer2":"数据分析师","answer3":"产品经理","correct_answer":"算法工程师"},{"question":["202304010005","pikaqiu的主人喜欢看的书籍是什么？",5],"answer1":"钢铁就是力量","answer2":"钢铁是怎样炼成的","answer3":"钢铁的未来","correct_answer":"钢铁就是力量"},{"question":["202304010006","pikaqiu的主人的主人叫什么名字？",6],"answer1":"小k","answer2":"小明","answer3":"小红","correct_answer":"小k"},{"question":["202304010007","pikaqiu的主人的主人是做什么的？",7],"answer1":"算法工程师","answer2":"数据分析师","answer3":"产品经理","correct_answer":"算法工程师"},{"question":["202304010008","pikaqiu的主人的主人喜欢看的书籍是什么？",8],"answer1":"钢铁就是力量","answer2":"钢铁是怎样炼成的","answer3":"钢铁的未来","correct_answer":"钢铁就是力量"},{"question":["202304010009","pikaqiu的主人的主人的主人叫什么名字？",9],"answer1":"小k","answer2":"小明","answer3":"小红","correct_answer":"小k"},{"question":["202304010010","pikaqiu的主人的主人的主人是做什么的？",10],"answer1":"算法工程师","answer2":"数据分析师","answer3":"产品经理","correct_answer":"算法工程师"},{"question":["202304010011","pikaqiu的主人的主人的主人喜欢看的书籍是什么？",1],"answer1":"钢铁就是力量","answer2":"钢铁是怎样炼成的","answer3":"钢铁的未来","correct_answer":"钢铁就是力量"},{"question":["202304010012","pikaqiu的主人的主人的主人的主人叫什么名字？",2],"answer1":"小k","answer2":"小明","answer3":"小红","correct_answer":"小k"},{"question":["202304010013","pikaqiu的主人的主人的主人的主人是做什么的？",3],"answer1":"算法工程师","answer2":"数据分析师","answer3":"产品经理","correct_answer":"算法工程师"},{"question":["202304010014","pikaqiu的主人的主人的主人的主人喜欢看的书籍是什么？",4],"answer1":"钢铁就是力量","answer2":"钢铁是怎样炼成的","answer3":"钢铁的未来","correct_answer":"钢铁就是力量"},{"question":["202304010015","pikaqiu的主人的主人的主人的主人的主人叫什么名字？",5],"answer1":"小k","answer2":"小明","answer3":"小红","correct_answer":"小k"},{"question":["202304010016","pikaqiu的主人的主人的主人的主人的主人是做什么的？",6],"answer1":"算法工程师","answer2":"数据分析师","answer3":"产品经理","correct_answer":"算法工程师"},{"question":["202304010017","pikaqiu的主人的主人的主人的主人的主人喜欢看的书籍是什么？",7],"answer1":"钢铁就是力量","answer2":"钢铁是怎样炼成的","answer3":"钢铁的未来","correct_answer":"钢铁就是力量"},{"question":["202304010018","pikaqiu的主人的主人的主人的主人的主人的主人叫什么名字？",8],"answer1":"小k","answer2":"小明","answer3":"小红","correct_answer":"小k"},{"question":["202304010019","pikaqiu的主人的主人的主人的主人的主人的主人是做什么的？",9],"answer1":"算法工程师","answer2":"数据分析师","answer3":"产品经理","correct_answer":"算法工程师"},{"question":["202304010020","pikaqiu的主人的主人的主人的主人的主人的主人喜欢看的书籍是什么？",10],"answer1":"钢铁就是力量","answer2":"钢铁是怎样炼成的","answer3":"钢铁的未来","correct_answer":"钢铁就是力量"}],"health_state":"health","attribute":"雷属性","name":"pikaqiu","level":"5","monster_image":"/character_images/placeholder-logo.png"}
# 初始化FastAPI
app = FastAPI(title=" BookMonster Agent API")

# 允许React前端跨域访问
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    # allow_origins=["http://localhost:8000"],
    allow_credentials=True,
    # allow_methods=["*"],
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)




def get_ollama_host() -> str:
    """Get the Ollama host from environment variables"""
    return os.getenv("OLLAMA_HOST", "http://localhost:11434")

def get_model_name() -> str:
    """Get the model name from environment variables"""
    return os.getenv("OLLAMA_MODEL", "qwen2.5vl:7b")

def get_chat_model_name() -> str:
    """Get the model name from environment variables"""
    return os.getenv("OLLAMA_CHAT_MODEL", "qwen2.5:3b")

def hash_to_6digit_sha256(s):
    """使用SHA256哈希到6位数字"""
    sha_hash = hashlib.sha256(s.encode()).hexdigest()
    sha_int = int(sha_hash, 16)
    return sha_int % 1000000

# Ollama配置
OLLAMA_BASE_URL = get_ollama_host()
OLLAMA_MODEL = get_model_name()

OLLAMA_CHAT_MODEL = get_chat_model_name()
print("OLLAMA_BASE_URL: ",OLLAMA_BASE_URL)
print("OLLAMA_MODEL: ",OLLAMA_MODEL)
print("OLLAMA_CHAT_MODEL: ",OLLAMA_CHAT_MODEL)

# class Environment():
#     def __init__(self) -> None:
#         super().__init__()
#         # load player init monster
#         pwd = os.getcwd()
#         root = "/".join(pwd.split("/")[:-1])
#         context = Context(root)
#         self.generation_agent = MultiModalAgent(model="qwen2.5vl:7b",
#                                 emb_model_name= "nomic-embed-text:latest",
#                                 tools=[],
#                                 timeout= 180,
#                                 context=context) 
#         self.scheduel_agent = Agent(context=context,model= "qwen2.5:7b",
#                                     emb_model_name = "nomic-embed-text:latest",
#                                     tools = tools_dict,
#                                     timeout= 180)
#         self.recog_agent = Agent(context=context,
#                                 model= "qwen2.5:3b",
#                                 emb_model_name = "nomic-embed-text:latest",
#                                 tools = tools_dict,
#                                 timeout= 180)
#         self.monsters = {}
#         self.task_queue = collections.defaultdict(list)
#         self.chunk_list = collections.defaultdict(list)
#         self.task_status = collections.defaultdict(dict)
#         self.current_task_id = None
#         # self.enermy_monsters_states.append(MonsterState(tmp_data))
# # env = Environment()



# 配置参数
UPLOAD_DIR = Path("uploads")
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB
ALLOWED_IMAGE_TYPES = ["image/jpeg", "image/png", "image/gif", "image/bmp"]
ALLOWED_AUDIO_TYPES = ["audio/wav", "audio/mpeg", "audio/ogg", "audio/mp4"]

# 创建上传目录
UPLOAD_DIR.mkdir(exist_ok=True)
(UPLOAD_DIR / "images").mkdir(exist_ok=True)
(UPLOAD_DIR / "audio").mkdir(exist_ok=True)

def save_upload_file(upload_file: UploadFile, subfolder: str) -> str:
    """保存上传的文件并返回文件路径"""
    # 生成唯一文件名
    file_ext = upload_file.filename.split('.')[-1] if '.' in upload_file.filename else ''
    unique_filename = f"{uuid.uuid4().hex}.{file_ext}"
    file_path = UPLOAD_DIR / subfolder / unique_filename
    
    # 保存文件
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(upload_file.file, buffer)
    
    return str(file_path)


class ImageItem(BaseModel):
    data: str  # Base64 编码的图像
    timestamp: str


class ImageRequest(BaseModel):
    image_data: List[ImageItem]  # Base64 编码的图像数据
    filename: str
    device_id: str
    timestamp: float
    total_images: int
    image_format: str = "png_base64"

# @app.post("/get_images_v1")
# async def get_image_v1( request:ImageRequest):

@app.post("/get_images_v1")
async def get_image_v1( request:ImageRequest):
    # print("request: ", request)
    try:
        print(f"Received image from {request.device_id}")
        print(f"Filename: {request.filename}")
        print(f"Total images in batch: {request.total_images}")
        
        # 解码 Base64 图像数据
        for image in request.image_data:
            image_bytes = base64.b64decode(image.data)
            print(f"Decoded image size: {len(image_bytes)} bytes")
            
            # 保存图像文件（可选）
            import os
            os.makedirs("uploads", exist_ok=True)
            
            filename = f"uploads/{request.device_id}_{int(image.timestamp)}.png"
            with open(filename, "wb") as f:
                f.write(image_bytes)
        
        print(f"Image saved as: {filename}")
        
        return {
            "status": "success",
            "message": "Image received successfully",
            "saved_path": filename,
            "received_at": time.time(),
            "device_id": request.device_id
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")


@app.post("/get_images")
async def get_image( images: List[UploadFile], timestamp:str, device_id:str):
    try:
        # 检查文件类型
        print("timestamp: ", timestamp)
        print("device_id: ", device_id)
        results = []
        batch_timestamp = datetime.now().isoformat()
        
        for image in images:
            if image.content_type not in ALLOWED_IMAGE_TYPES:
                continue  # 跳过不支持的格式
                
            file_path = save_upload_file(image, "images")
            
            results.append({
                "original_filename": image.filename,
                "saved_path": file_path,
                "file_size": os.path.getsize(file_path),
                "status": "success"
            })
        
        # 保存文件
        # file_path = save_upload_file(image, "images")

        # Save data to VectorDB here
        
        # 构建响应数据
        # response_data = {
        #     "status": "success",
        #     "message": "图片上传成功",
        #     "filename": image.filename,
        #     "saved_path": file_path,
        #     "file_size": os.path.getsize(file_path),
        #     "device_id": device_id,
        #     "timestamp": timestamp or datetime.now().isoformat()
        # }

        response_data = {"success": True,"message":f"saved to {file_path} size: {len(results)}"}
        return JSONResponse(content=response_data, status_code=200)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"文件上传失败: {str(e)}")







@app.post("/chat")
async def chat(request : dict):
    # chat dialog task.
    """
    调用Ollama生成回复
    输入request:
        {
            "pdf_path": "pdf path",
            "image_path": "image path",
            "prompt": "description",
        }
    
    最终输出response 格式示例：
    {
        "status": "success",
        response: 
    }

    """
    response = {
       "status":"success",
       "response": ""
    }
    print("chat request: ", request)

    image_path = request.get("image_path","")
    file_path = request.get("file_path","")
    if file_path:
        request['pdf_path'] = os.path.join("/home/wwk/workspace/ai_project/KnowledgeMaster/front-end-react-v3",file_path)
    if image_path:
        request['image_path'] = os.path.join("/home/wwk/workspace/ai_project/KnowledgeMaster/front-end-react-v3",image_path)
    request['file_path'] = request.get('pdf_path',"")
    print("request: ", request)

    try:
        response = await env.pipeline(request)
    except Exception as e:
        # raise HTTPException(status_code=422, detail=f"生成失败: {str(e)}")
        logging.error(f"chat error: {str(e)}")
        raise HTTPException(status_code=422, detail=f"chat failed:  {str(e)}")
    return response








@app.post("/chat_v2")
async def chat_v2(
    pdf_path: UploadFile = File(...),
    prompt: str="",
    image_path: UploadFile = File(...)
):
    # chat dialog task.
    """
    调用Ollama生成回复
    输入request:
        {
            "pdf_path": "pdf path",
            "image_path": "image path",
            "prompt": "description",
        }
    
    最终输出response 格式示例：
    {
        "status": "success",
        response: 
    }

    """
    response = {
       "status":"success",
       "response": ""
    }


    file_content = await pdf_path.read()
    file_path = f"../front-end-react-v3/public/uploads/{pdf_path.filename}"
    
    
    
    
    image_content = await image_path.read()
    image_path_str = f"../front-end-react-v3/public/uploads/{image_path.filename}"
    

    with open(file_path, "wb") as f:
        f.write(file_content)
    print(f"file_path: {file_path} written")
    
    with open(image_path_str, "wb") as f:
        f.write(image_content)
    
    print(f"image_path: {image_path_str} written")
    
    request = {
        "pdf_path": file_path,
        "image_path": image_path_str,
        "prompt": prompt,
    }
    print("chat request: ", request)

    image_path = request.get("image_path","")
    file_path = request.get("file_path","")
    if file_path:
        request['pdf_path'] = os.path.join("/home/wwk/workspace/ai_project/KnowledgeMaster/front-end-react-v3",file_path)
    if image_path:
        request['image_path'] = os.path.join("/home/wwk/workspace/ai_project/KnowledgeMaster/front-end-react-v3",image_path)
    print("request: ", request)

    try:
        response = await env.pipeline(request)
    except Exception as e:
        # raise HTTPException(status_code=422, detail=f"生成失败: {str(e)}")
        logging.error(f"chat error: {str(e)}")
        raise HTTPException(status_code=422, detail=f"chat failed:  {str(e)}")
    return response





# 调试接口（打印原始请求）
@app.post("/api/debug")
async def debug_endpoint(raw_request: dict):
    print("收到的原始请求:", raw_request)
    return {"debug_data": raw_request}

if __name__ == "__main__":
    # # Debug
    # port = 8000
    # from pyngrok import ngrok
    # # 使用 ngrok 连接指定端口，获取公共 URL
    # # 这里假设你已经按照前面的方法设置了 NGROK_AUTH_TOKEN（推荐）
    # # 如果没有，以下代码仍会运行，但每次连接的 URL 都会变化且有限制
    # public_url = ngrok.connect(port, bind_tls=True).public_url
    print(f" * Public URL: {public_url}")
    import uvicorn
    os.makedirs("uploads", exist_ok=True)
    os.makedirs("generated_images", exist_ok=True)
    os.makedirs("logs", exist_ok=True)
    
    # 启动大模型自动规划后台线程， 让大模型自己决定什么时候调用起自己进行学习总结
    uvicorn.run(app, host="0.0.0.0", port=8000)