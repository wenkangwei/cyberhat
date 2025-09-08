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
from agent import *
import asyncio
from constant import *
from tools.utils import *
# # Debug

from tools.webpage_crawler import webpage_crawler
from pyngrok import ngrok
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
    allow_origins=["http://localhost:8000"],
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

class Environment():
    def __init__(self) -> None:
        super().__init__()
        # load player init monster
        pwd = os.getcwd()
        root = "/".join(pwd.split("/")[:-1])
        context = Context(root)
        self.generation_agent = MultiModalAgent(model="qwen2.5vl:7b",
                                emb_model_name= "nomic-embed-text:latest",
                                tools=[],
                                timeout= 180,
                                context=context) 
        self.scheduel_agent = Agent(context=context,model= "qwen2.5:7b",
                                    emb_model_name = "nomic-embed-text:latest",
                                    tools = tools_dict,
                                    timeout= 180)
        self.recog_agent = Agent(context=context,
                                model= "qwen2.5:3b",
                                emb_model_name = "nomic-embed-text:latest",
                                tools = tools_dict,
                                timeout= 180)
        self.monsters = {}
        self.task_queue = collections.defaultdict(list)
        self.chunk_list = collections.defaultdict(list)
        self.task_status = collections.defaultdict(dict)
        self.current_task_id = None
        # self.enermy_monsters_states.append(MonsterState(tmp_data))
    
    def compute_batch_chunk_data(self, task_id, prompt, chunk, chunk_ids,debug=False):
        if len(chunk) != len(chunk_ids):
            print("len(chunk)  != len(chunk_ids) ", len(chunk) , ", ", len(chunk_ids))
            return [] 


        # prompt = template2
        chunk_emb = self.generation_agent.gen_embedding(chunk)
        chunk_batch = "\n".join(chunk)
        msg = {'role': "user",
                    'content': prompt + "\n" + chunk_batch }
        qa = asyncio.run(self.generation_agent.chat([msg]))
        # 存储到队列
        response_str = qa.replace("```json\n", '').replace("```", '')
        parsed_qa = json.loads(response_str)
        if not parsed_qa or not chunk_emb  or not response_str:
            print("Invalid Points from LLM: ", response_str)
            return []
        if debug:
            print("response_str: ",qa)
            print("chunk_ids: ", chunk_ids)
            print("parsed repsonse: ", parsed_qa)
        res = []
        for i, chunk_id in enumerate(chunk_ids):
            # filter cases which are ignored by LLM
            if chunk_id in parsed_qa:
                points = parsed_qa[chunk_id].get("points",[])
                for v in points:
                    v['point_id'] = str(task_id)+"_"+ str(chunk_id).lower()
                data = {
                    "book_id": str(task_id).lower(),
                    "chunk_id": str(chunk_id).lower(),
                    "emb_id": str(task_id)+"_"+ str(chunk_id).lower(),
                    "chunk_emb": chunk_emb[i],
                    "points":points,
                    'content': chunk[i]
                }
                res.append(data)
        return  res

    def generate_qa(self, task_id, book_nm, chunks, prompt, request):
        f"""模拟大模型分批处理PDF
        task_id: 对应数据库id 或者名称 用于es 里面的index_name
        chunks: list of dictionary data
        prompt: prompt for llm

        #书籍结构
            book:
                book_id
                chunks:
                    chunk_id1:
                        emb_id
                        emb_vector
                        points:
                            point1, difficulty
                            point2, difficulty
                            point3, difficulty
                    chunk_id2
                    chunk_idn

        """
        
        self.task_queue[task_id] = []
        self.task_status[task_id] = {"status": "running"}
        self.current_task_id = task_id
        # test elastic search
        # book_id = 'mmoe.pdf'
        # test_data = {
        #     "1234": {
        #     "chunk_id": "1234",
        #     "emb_id": "mmoe.pdf_1234",
        #     "content": "React组件从创建到销毁的完整过程，包括挂载、更新和卸载三个阶段。",
        #     "points": [
        #     { "point": "组件挂载过程", "difficulty": "中级" },
        #     { "point": "状态更新机制", "difficulty": "中级" },
        #     { "point": "性能优化技巧", "difficulty": "高级" },
        #     ],
        # },

        # "45678":{
        #     "chunk_id": "45678",
        #     "emb_id": "mmoe.pdf_44567",
        #     "content": "6666React组件从创建到销毁的完整过程，包括挂载、更新和卸载三个阶段。",
        #     "points": [
        #     { "point": "挂载过程", "difficulty": "中级" },
        #     { "point": "状态机制", "difficulty": "中级" },
        #     { "point": "性能技巧", "difficulty": "高级" },
        #     ],
        # },
        # }

        # print("Create Doc..")
        # ret = self.generation_agent.memory_client.es_client.batch_create_doc(book_id, test_data)
        # print("Searching Doc.. : ", book_id)
        # # result = self.generation_agent.memory_client.es_client.search(index= book_id, keyword=book_id, fields=['_index','_id'])
        # # result = self.generation_agent.memory_client.es_client.get_all_documents_search_after(book_id)
        # result = self.generation_agent.memory_client.es_client._get_all_documents_scroll(book_id)
        # print("test search result: ", result)

        try:
            print("start generate_qa")
            # 这里是你的PDF解析逻辑，改为分批处理
            chunk_batch_ls = []
            chunk_id_ls = []
            embeddings_ls = collections.defaultdict(list)
            batch_size = 2 #不批量处理
            debug = False
            id_content_map = []
            for i, chunk in enumerate(chunks):
                chunk_id = i+1
                chunk['chunk_id'] = f"chunk{chunk_id}"
                chunk['task_id'] = str(task_id).lower() 
                chunk_data = None
                chunk_name = book_nm + ":" + chunk['title']
                chunk_batch_ls.append( f"###chunk{chunk_id}: \n" + chunk['content'])
                chunk_id_ls.append(f"chunk{chunk_id}")
                self.chunk_list[task_id].append(chunk)
                if chunk_id > 6:
                    break
                # batch processing chunk data to get embedding, embedding ids and question list
                try:
                    if (i%batch_size == 0) or len(chunks) - chunk_id <= batch_size:
                        print("generating qa when i=",i)
                        debug = True if i<6 else False
                        chunk_data = self.compute_batch_chunk_data(task_id, prompt, chunk_batch_ls, chunk_id_ls, debug)
                        chunk_batch_ls.clear()
                        chunk_id_ls.clear()

                        # filter invalid data
                        if not chunk_data:
                            continue
                    
                        # parse data
                        if i <10:
                            print("chunk_data: ", [[d['points'], d['emb_id'], len(d['chunk_emb'])] for d in chunk_data ])
                        
                        for data in chunk_data:
                            emb_id = data['emb_id']
                            emb = data.pop("chunk_emb")
                            content = data['content']
                            id_content_map.append( {"emb_id": emb_id, "content":content}) 
                            embeddings_ls["emb_id"].append(emb_id) 
                            embeddings_ls["chunk_emb"].append(emb) 
                            data['book_name'] = book_nm
                            data['chunk_name'] = chunk_name
                            # self.task_queue[task_id].extend(data['points'])
                            self.task_queue[task_id].append(data)
                        print(f"Task {task_id} - 已处理 {chunk_id} chunks 和 {len( self.task_queue[task_id])} 条QA")
                except Exception as e:
                    print("Chunk Loop Exception: ", str(e))
                    if chunk_data and len(chunk_data)>0:
                        print(" Problem with chunk_data: ", [[d['points'], d['emb_id'], len(d['chunk_emb'])] for d in chunk_data ])
                    continue
            
            print(f"task_queue[{task_id}] total size: ", len(self.task_queue[task_id]))
            # save faiss vectors
            print("saving embeddings with size: ",len( embeddings_ls['chunk_emb']), "emb_id size: ",len(embeddings_ls["emb_id"]))
            assert len( embeddings_ls['chunk_emb']) == len(embeddings_ls["emb_id"]), "chunk emb size is not equal to emb_id size"
            self.generation_agent.save_embedding( embeddings_ls['chunk_emb'], embeddings_ls["emb_id"], merge_index=False)
            # self.generation_agent.memory_client.memory.save([v['content'] for v in id_content_map], id_content_map)
            # save generated questions- answers pair to es. Don't save origin text for saving storage
            print("Saving data to elastic search")
            doc_dict= {}
            # index_name = book_id
            index_name = str(task_id).lower()
            for _, doc in enumerate(self.task_queue[task_id]):
                doc_id = doc['emb_id']
                doc_dict[doc_id] = doc
            
            book_desc = chunks[0]['content']
            book_title = chunks[0]['title']
            if not book_desc:
                book_desc = chunks[0]['title']
            book_desc = asyncio.run(self.scheduel_agent.chat_with_tools([{"role": "user", "content": "请对下面内容用中文100字内进行总结\n"+book_desc}], tools_dict)) 
            print("Book_name: ", book_nm, ", book_desc: ", book_desc, "index_name: ", index_name)
            ret = self.generation_agent.memory_client.es_client.batch_create_doc(index_name, doc_dict, book_nm, book_desc)
            print("QA doc Saved with ret = ", ret)

            
            rec_email = self.scheduel_agent.context.config.get("user_profile",{}).get("email", "1904832812@qq.com")
            print("Sending email to ", rec_email)
            #Send email to user
            email_info = f"""请调用tools发送邮件到 {rec_email} 提醒用户来APP回顾知识库。
            请你根据下面知识库的信息取一个合适的邮件title， 并且title以 ‘KnowledgeMaster-’ 开头<这里填入你的>。 邮件的body应该根据知识库信息写一段吸引人的内容
            邮件要是HTML 格式，必须以<html> 开头， 以 </html>结尾
            以下是知识库的信息：
            - 知识库书名: {book_nm}
            - 知识库APP链接: {public_url}
            - 知识库第一段文本: {book_title +"\n" + book_desc} 
            """
            chat_message=[
                {"role": "system", "content": "你是一个知识库助手，能解析用户知识库后通过发送邮件给用户， 有必要的话可以调用提供给你的tools"},
                {"role": "user", "content": email_info}
            ]
            print("email_info = \n", email_info)
            res = asyncio.run(self.scheduel_agent.chat_with_tools(chat_message, tools_dict)) 
            print("chat_with_tools res = ", res)
           
        except Exception as e:
            print("generate_qa Exception: ", str(e))
            self.task_status[task_id] = {"error": str(e), "status":"failed"}
        finally:
            print("finally")
            self.task_status[task_id] = {"completed": True, "status":"completed"}
    
    async def intention_recog(self, inputs:str):
        prompt = """
        你是一个意图识别专家， 你能通过下面用户发送的请求识别到用户需要什么功能.
        下面有几个支持的功能
        1. generation_cards: 用户需要把文档文件/图片/需要总结的文字/网页链接 多种数据上传然后调用我们这边的生成知识卡片的功能
        2. chat: 用户需要对以往生成的知识卡片进行复习,或者聊天服务
        3. unkown: 如果你识别不出来，就返回unknown
        返回格式要求：
        1. 你只能以下面的json格式返回，以'{'开始 以'}'结尾， 并且json里的key有option和urls
            json格式： {"option": "", "urls": []} 
        2. option的值你只能从返回这个列表[generation_cards, chat, unknown]里的其中一个选项， 不能返回任何无关的字符内容
        3. urls的值是一个list, 你准确提取要把用户输入的内容里要解析的一个或多个url, 并把url以字符串形式放到这个list里面。 如果找不到url， 就返回空list
        """
        result= await self.recog_agent.chat([{"role":"system", "content": prompt},
                                {"role":"user", "content":inputs}
                                ])
        result = result.strip()
        log_operation(f"result:", result)
        # res = result.strip().replace("~~~", "")
        res = result.strip().replace("```json\n", '').replace("```", '')
        result = json.loads(res)
        if result.get("option", "") not in  ["generation_cards",'chat', "unknown"]:
            result['option'] = "unknown"
        return result
    
    def search(self, query):
        """
        [{ "content": chunk content,
            "point": key point,
            "difficulty": 1 
        }]
        """
        contents = self.generation_agent.memory_client.memory.search(query, top_n=10, unique=True)
        points = self.generation_agent.memory_client.es_client.search(index, query,fields=['point','content'])
        return points

    async def generate_cards(self, request : dict):
        """
        调用Ollama生成回复
        输入request:
            {
                "pdf_path": "pdf path",
                "image_path": "image path",
                "prompt": "description",
                "email": "user email"
            }
        
        最终输出response 格式示例：
        {
            "status": "success",
            response: ""
        }

        [
            {
            "database": "database_name",
            "card_id": "card_id",
            "points":[
            {"point": "content1",
            "difficulty": "difficulty"},
            {"point": "content2",
            "difficulty": "difficulty"},
            ]
            }
        ]
        """
        ret_response = {
        "status":"success",
        "response": ""
        }
        print("generate monster request: ", request)
        images = request.get('images_path',"")
        prompt = request.get('prompt_path', "")
        pdf_path = request.get('pdf_path',"")
        try:
            print("Processing generate_cards..")
            log_operation("Processing generate_bookmonster prompt:", prompt)


            kl_card_template="""
             最高优先级要求: 
        1. 你只能按照下面的JSON格式输出并填写内容， 不要输出任何非json格式的内容。输出只能是{符合开头,  以}符合结尾
        2. 输入格式: 用户输入的多个chunk以 ###chunk开头， 比如###chunk1 就代表chunk_id就是 chunk1.  之后跟着chunk的内容. 以此类推去提取每个chunk的chunk_id和对应内容
        3. 任务: 你要准确识别每个chunk 并且对每个chunk的内容进行精简地提取出3条关键具体知识点。如果知识点有数据支持请把重要数据也放到总结里。每个知识点用1-2句话总结。 这些知识点被放到 “points”列表里
        3. "points" 列表里每条json含有 point， difficulty字段分别对应知识点，以及知识点难度。知识点难度从1-10 数字范围里取，1表示最简单，10表示最难。
        4. 每条知识点不能重复。
        5. 下面是给你的参考返回例子的格式：
        {
                “chunk1”:{
                    "points": [{"point":"", "difficulty":"1"},
                                {"point":"", "difficulty":"2"},
                    ]
                },
                “chunk2”:{
                    "points": [{"point":"", "difficulty":"3"},
                                {"point":"", "difficulty":"4"},
                    ]
                }
                    
        }
            """
            
            # 调用Ollama的生成API
            print("kl_card_template:  ", kl_card_template)
            # parse URLs
            url_sections = []
            sections= []
            book_nm = ""
            for url in request.get("urls",[]):
                url_res = await webpage_crawler(url, output_file="", mode="wechat")
                if url_res and 'title' in url_res:
                    print("url_res title: ", url_res['title'], "\n url_res[content]: ", url_res['content'][:20])
                    book_nm = book_nm + url_res['title']
                    url_sections.append(url_res)
            # parse PDF
            if pdf_path:
                book_nm= pdf_path.split("/")[-1]
                sections = self.generation_agent.parse_file(pdf_path)
                print("section size: ", len(sections), "\n section[0]: ", sections[0])
            book_id = hash_to_6digit_sha256(book_nm)
            
            # await gb_state.generate_batch_qa(task_id, sections,template2)
            print("Response result:", str(ret_response))
            sections = url_sections + sections
            thread = threading.Thread(target=self.generate_qa, args=(book_id,book_nm, sections,kl_card_template, request))
            thread.start()
            ret_response["response"] = "generating knowledge cards. Please wait for few seconds."
            logging.info(f"response: {ret_response}" )
        except Exception as e:
            logging.error(f"generation error: {str(e)}")
            raise HTTPException(status_code=422, detail=f"生成失败: {str(e)}")
        return ret_response

    async def pipeline(self, request: dict):
        inputs = str(request)
        response = {
            "response":"",
            "card_list":[],
            "status":"success"
        }
        chat_message = []
        intention_res = await self.intention_recog(inputs)
        recog_res = intention_res.get("option", "unknown")
        request['urls'] = intention_res.get("urls",[])
        if recog_res ==  "generation_cards":
            if not self.current_task_id or self.task_status[self.current_task_id].get("status","") != "running":
                print("start generation task in background")
                # start generation task in background
                await self.generate_cards(request)
                # return response
                response['response'] = f"开始帮您生成知识库中 task_id: {self.current_task_id} 请稍候再请求生成。 可以先聊聊别的哦~"
                return response
            else:
                print(" generation_cards task is still running in background")
                # return pending response
                status = self.task_status[self.current_task_id]
                response['response'] = f"上个任务还在跑呢 task_id: {self.current_task_id} status: {status}。 可以先聊聊别的哦~"
                return response
        elif recog_res ==  "chat":
            print("start chatting task")
            # use chat with rag tools to search note card
            chat_message.extend([
                {"role": "system", "content": "你是一个知识库助手，能够准确识别用户想要查询的知识点，解答用户问题， 有必要的话可以调用提供给你的tools"},
                {"role": "user", "content": request.get("prompt","")}
            ])
            res = await self.scheduel_agent.chat_with_tools(chat_message, tools_dict)
            response['response']= res
            pass
        # elif recog_res == "unknown":
        else:
            print("get unknown chatting task")
            # simply chat
            chat_message.extend([
                {"role": "user", "content": request.get("prompt","")}
            ])
            res = await self.scheduel_agent.chat_with_tools(chat_message,tools_dict)
            response['response']= res
            pass
        # else:
        #     response['status'] = "failed"
        #     response['msg'] = "Unknown request type"
        return response


    
env =  Environment()

def log_operation(action: str, details: str, object_id: str = None, level: str = "info"):
    """日志记录到文件和控制台"""
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "action": action,
        "details": details,
        "object_id": object_id
    }
    
    os.makedirs("logs", exist_ok=True)
    log_file = f"logs/operations_{datetime.now().strftime('%Y-%m-%d')}.log"
    
    with open(log_file, "a") as f:
        f.write(f"{log_entry}\n")
    
    getattr(logging, level)(f"{action}: {details}")


class DatabaseListRequest(BaseModel):
    key: Optional[str] = "database"

@app.post("/get_database_list")
async def database_list(request:dict):
    resp = {"status":"success", "msg":"", "index_list":[]}
    print("request: ",request)
    try:
        index_list = env.generation_agent.memory_client.es_client.get_all_index_values()
        result = []
        for book_id in index_list:
            cards = env.generation_agent.memory_client.es_client._get_all_documents_scroll(book_id)
            if len(cards)>0:
                result.append({"book_id": book_id, "book_name": cards[0].get('_index_name',""), "description":  cards[0].get('_index_description',"")})
        resp['index_list'] = result
        print("database_list: ", result)
        return resp
    except Exception as e:
        logging.error(f"Failed to load database list error: {str(e)}")
        raise HTTPException(status_code=422, detail=f"database_list failed:  {str(e)}")
        resp['status'] = "failed"
        resp['msg'] = str(e)
        return resp


@app.post("/delete_books_list")
async def delete_books_list(request : dict):
    resp = {"status":"success", "msg":""}
    try:
        indices = request['indices']
        response = env.generation_agent.memory_client.es_client.delete_indices(indices)
        print("delete_books_list response: ",response)
    except Exception as e:
        logging.error(f"delete_books_list failed:  {str(e)}")
        raise HTTPException(status_code=422, detail=f"delete_books_list failed:  {str(e)}")
    return resp
    

class CardListRequest(BaseModel):
    book_id: str

@app.post("/get_card_list")
async def get_card_list(request : dict):
    """
    request:
        {"book_id": "id"}
    response:
        {"status":"success", msg:"" ,"card_list": [{"card1":{"points":[{"point":"", "difficulty"},{"point":"", "difficulty"}]} }]}
    """
    # return generated  knowledge index list
    #切换到获取知识库tab 时调用
    # result = self.generation_agent.memory_client.es_client.search(index= book_id, keyword=book_id, fields=['_index','_id'])
    # result = self.generation_agent.memory_client.es_client.get_all_documents_search_after(book_id)
    resp = {"status":"success", "msg":"", "card_list":[]}
    print("Get get_card_list request: ", request)
    try:
        book_id = request['book_id']
        result = env.generation_agent.memory_client.es_client._get_all_documents_scroll(book_id)
        resp["msg"]=""
        resp['card_list']= [ r["doc"] for r in result]
    except Exception as e:
        logging.error(f"get_card_list failed:  {str(e)}")
        raise HTTPException(status_code=422, detail=f"get_card_list failed:  {str(e)}")
        
    return resp

@app.post("/get_card_recom_realtime")
async def get_card_recom_realtime(request : dict):
    # return cards of selected knowledge set
    # 请求大模型提取自主推荐cards 到用户邮箱 以及推荐列表

    return

class CardRecomRequest(BaseModel):
    key: Optional[str] = "" 

@app.post("/get_card_recom")
async def get_card_recom(request : CardRecomRequest):
    # return cards of selected knowledge set
    # 请求大模型提取自主推荐cards 到用户邮箱 以及推荐列表
    resp = {"status":"success", "msg":"", "card_list":[]}
    print("Get request: ", request)
    try:
        book_list = env.generation_agent.memory_client.es_client.get_all_index_values()
        for book_id in book_list:
            result = env.generation_agent.memory_client.es_client._get_all_documents_scroll(book_id)
            resp["msg"]=""
            resp['card_list'].extend([ r["doc"] for r in result])
    except Exception as e:
        logging.error(f"get_card_recom failed:  {str(e)}")
        raise HTTPException(status_code=422, detail=f"get_card_list failed:  {str(e)}")
        
    return resp


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
    uvicorn.run(app, host="localhost", port=8000)