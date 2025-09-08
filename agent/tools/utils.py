# src/utils.py (部分)
import inspect
import json
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import os
from common.context import Context

def function_to_json(func) -> dict:
    # ... (函数实现细节)
    # 返回符合 OpenAI tool schema 的字典
    return {
        "type": "function",
        "function": {
            "name": func.__name__,
            "description": inspect.getdoc(func),
            "parameters": {
                "type": "object",
                "properties": parameters,
                "required": required,
            },
        },
    }



def get_current_weather(location, unit="celsius"):
    """
    {
        "type": "function",
        "function": {
            "name": "get_current_weather",
            "description": "获取天气信息API调用",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "城市名称"
                    }
                },
                "required": ["location"]
            }
        }
    }
    """
    print(f"正在获取 {location} 的天气（单位: {unit}）")
    return json.dumps({
        "location": location,
        "temperature": "22",
        "unit": unit,
        "forecast": ["晴朗"]
    })

# def send_email(recipient:str, subject:str, body:str) ->json:
#     """{
#         "type": "function",
#         "function": {
#             "name": "send_email",
#             "description": "发送邮件",
#             "parameters": {
#                 "type": "object",
#                 "properties": {
#                     "recipient": {
#                         "type": "string",
#                         "description": "收件人邮箱"
#                     },
#                     "subject": {
#                         "type": "string",
#                         "description": "邮件主题"
#                     },
#                     "body": {
#                         "type": "string",
#                         "description": "邮件内容"
#                     }
#                 },
#                 "required": ["recipient"]
#             }
#         }
# }
#     """
#     print(f"发送邮件给 {recipient}，主题: {subject}")
#     print(f"内容: {body}")
#     return json.dumps({"status": "success", "message": "邮件已发送"})




def send_email(recipient:str, subject:str, body:str) ->json:
    """{
        "type": "function",
        "function": {
            "name": "send_email",
            "description": "发送邮件",
            "parameters": {
                "type": "object",
                "properties": {
                    "recipient": {
                        "type": "string",
                        "description": "收件人邮箱"
                    },
                    "subject": {
                        "type": "string",
                        "description": "邮件主题"
                    },
                    "body": {
                        "type": "string",
                        "description": "邮件内容"
                    }
                },
                "required": ["subject","recipient","body"]
            }
        }
}
    """
    print(f"发送邮件给 {recipient}，主题: {subject}")
    print(f"内容: {body}")
    # 验证必要参数
    required_keys = ['sender_email', 'password', 'smtp_server', 'port', 
                    'receiver_email', 'subject', 'message']
    pwd = os.getcwd()
    root = "/".join(pwd.split("/")[:-1])
    context = Context()
    config = context.config['tools']['email']
    pw = config['password']
    if str(pw).startswith("<") and str(pw).endswith(">"):
        env_var = str(pw).replace("<","").replace(">","").strip()
        password = os.environ.get(env_var, "")
    else:
        password = str(pw)
    print("email password: ", password)
    config['message'] = body
    config['subject'] = subject
    config['receiver_email'] = recipient

    sender_email = config['sender_email']  # 替换为您的QQ邮箱
    # password = config['password']  # 替换为您的授权码，不是登录密码！
    smtp_server = config['smtp_server']
    receiver_email = config['receiver_email']
    port = 587  # 对于QQ邮箱使用587端口
    for key in required_keys:
        if key not in config:
            raise ValueError(f"缺少必要参数: {key}")
    
    # 创建邮件
    msg = MIMEMultipart()
    
    msg["From"] = config['sender_email']
    msg["To"] = config['receiver_email']
    msg["Subject"] = config['subject']
    
    # 添加邮件正文
    text_type = "plain" if not body.startswith("<html>") else "html"
    msg.attach(MIMEText(body, text_type))
    
    
    try:
        # 创建安全连接
        context = ssl.create_default_context()
        
        # 连接服务器并发送邮件
        # with smtplib.SMTP_SSL(smtp_server) as server:
        with smtplib.SMTP(smtp_server, port) as server:
            server.ehlo()
            server.starttls(context=context)
            server.ehlo()
            print("loging ...")
            server.login(sender_email, password)
            print("sending mail")
            server.sendmail(sender_email, receiver_email, msg.as_string())
            print("quit")
            server.quit()
        
        print("邮件发送成功!")
        # return True
        return json.dumps({"status": "success", "message": "邮件已发送"})
        
    except Exception as e:
        print(f"发送失败: {str(e)}")
        # return False
        return json.dumps({"status": "failed", "message": str(e)})
    


def gen_tools_desc(funcs):
    from inspect import signature
    res = []
    for func in funcs:
        func_desc = func.__doc__
        # sig = signature(func)
        # print("func signature: ",sig)
        # print("Parameters:  ",sig.parameters['recipient'])
        # print("sig.parameters['recipient']: ", type(sig.parameters['recipient']))
        # print("Return annotation:  ",sig.return_annotation)
        # template = template.format(func.__name__, func.__doc__, sig.parameters['recipient'])
        print(func_desc)
        res.append(json.loads(func_desc))
    return res


def gen_tools_dict(funcs):
    from inspect import signature
    tool_desc = []
    tool_funcs = {}
    for func in funcs:
        func_desc = func.__doc__
        func_desc_json = json.loads(func_desc)
        try:
            func_name = func_desc_json["function"].get("name")
            print("func_name info: ")
            print(func_name)
        except Exception as e:
            raise ValueError(f"Function doc description must be JSON format and contain key 'function' Got e= {e}")
        tool_funcs[func_name] = func
        tool_desc.append(func_desc_json)
    tools_dict = {
            "tools_desc": tool_desc,
            "tools_func": tool_funcs
        }
    return tools_dict


# sig = signature(send_email)
# print("send_email signature: ",sig)
# print("Parameters:  ",sig.parameters)
# print("Return annotation:  ",sig.return_annotation)
tools_dict = gen_tools_dict([send_email, get_current_weather])
print("tools_dict: ", tools_dict)
# tools_des =gen_tools_desc([send_email, get_current_weather])
# print("gen_tools_desc: ", tools_des)
# tools_func= {
#         "get_current_weather": get_current_weather,
#         "send_email": send_email
# }

# tools_dict = {
#     "tools_desc": tools_des,
#     "tools_func": tools_func
# }


# send_email("1904832812@qq.com", "Hello world", "Hello World")