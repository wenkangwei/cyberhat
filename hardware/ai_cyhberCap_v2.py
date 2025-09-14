import network
import socket
import os,time
import requests


import asyncio
from libs.PipeLine import PipeLine
from libs.AIBase import AIBase
from libs.AI2D import Ai2d
from libs.Utils import *
import os,sys,ujson,gc,math,random,time
import ulab.numpy as np
import image
import aidemo
import requests
import io
import ubinascii
import base64


from libs.PipeLine import ScopedTiming
from media.pyaudio import *                     # 音频模块
from media.media import *                       # 软件抽象模块，主要封装媒体数据链路以及媒体缓冲区
import media.wave as wave                       # wav音频处理模块
import nncase_runtime as nn                     # nncase运行模块，封装了kpu（kmodel推理）和ai2d（图片预处理加速）操作
import ulab.numpy as np                         # 类似python numpy操作，但也会有一些接口不同
import aidemo                                   # aidemo模块，封装ai demo相关前处理、后处理等操作
import time                                     # 时间统计
import struct                                   # 字节字符转换模块
import gc                                       # 垃圾回收模块
import os,sys                                   # 操作系统接口模块







import _thread  # 多线程 语音+ 视频
pl=None
p=None
SSID = "HONOR 90 Pro"        # 路由器名称
PASSWORD = "rts8z7naqyh352v" # 路由器密码
#SERVER_URL="http://172.22.48.1:8000"
#SERVER_URL="http://172.22.61.219:8000"

## 局域网ip
SERVER_URL="http://192.168.112.123:8000"
THRESH = 0.5                # 检测阈值
SAMPLE_RATE = 16000         # 采样率16000Hz,即每秒采样16000次
CHANNELS = 1                # 通道数 1为单声道，2为立体声
FORMAT = paInt16            # 音频输入输出格式 paInt16
CHUNK = int(0.3 * 16000)
RATE=SAMPLE_RATE

lock = _thread.allocate_lock()
# 初始化音频预处理接口
fp = aidemo.kws_fp_create()
p = PyAudio()
p.initialize(CHUNK)    #初始化PyAudio对象
display_mode="hdmi"
rgb888p_size=[224,224]
# 模型路径
# kmodel_path="/sdcard/examples/kmodel/yolov8n_224.kmodel"
# 其它参数设置
confidence_threshold = 0.3
nms_threshold = 0.4
max_boxes_num = 30
# 初始化PipeLine
pl=PipeLine(rgb888p_size=rgb888p_size,display_mode=display_mode)
pl.create()

send_lock=False

# filename = save_wav_file = "/sdcard/examples/test_audio_v1.wav"
# duration = 15




def network_use_wlan(is_wlan=True):
    if is_wlan:
        sta=network.WLAN(0)
        sta.connect(SSID,PASSWORD)
        print(sta.status())
        while sta.ifconfig()[0] == '0.0.0.0':
            os.exitpoint()
        print(sta.ifconfig())
        ip = sta.ifconfig()[0]
        return ip
    else:
        a=network.LAN()
        if not a.active():
            raise RuntimeError("LAN interface is not active.")
        a.ifconfig("dhcp")
        print(a.ifconfig())
        ip = a.ifconfig()[0]
        return ip

def get(url=''):
    network_use_wlan(True)
    if not url:
        url = "https://micropython.org/ks/test.html"
    headers = {"Host": "http://micropython.org"}
    #    r = requests.get(url, headers=headers, timeout=120)
    r = requests.get(url, timeout=120)
    print("status:", r.status_code)
    print(r.text) # 或 r.content 取 bytes
    r.close()



def exit_check():
    try:
        os.exitpoint()
    except KeyboardInterrupt as e:
        print("user stop: ", e)
        return True
    return False



# 自定义关键词唤醒类，继承自AIBase基类
class KWSApp(AIBase):
    def __init__(self, kmodel_path, threshold, debug_mode=0):
        super().__init__(kmodel_path)  # 调用基类的构造函数
        self.kmodel_path = kmodel_path  # 模型文件路径
        self.threshold=threshold
        self.debug_mode = debug_mode  # 是否开启调试模式
        self.cache_np = np.zeros((1, 256, 105), dtype=np.float)

    # 自定义预处理，返回模型输入tensor列表
    def preprocess(self,pcm_data):
        pcm_data_list=[]
        # 获取音频流数据
        for i in range(0, len(pcm_data), 2):
            # 每两个字节组织成一个有符号整数，然后将其转换为浮点数，即为一次采样的数据，加入到当前一帧（0.3s）的数据列表中
            int_pcm_data = struct.unpack("<h", pcm_data[i:i+2])[0]
            float_pcm_data = float(int_pcm_data)
            pcm_data_list.append(float_pcm_data)
        # 将pcm数据处理为模型输入的特征向量
        mp_feats = aidemo.kws_preprocess(fp, pcm_data_list)[0]
        mp_feats_np = np.array(mp_feats).reshape((1, 30, 40))
        audio_input_tensor = nn.from_numpy(mp_feats_np)
        cache_input_tensor = nn.from_numpy(self.cache_np)
        return [audio_input_tensor,cache_input_tensor]

    # 自定义当前任务的后处理，results是模型输出array列表
    def postprocess(self, results):
        with ScopedTiming("postprocess", self.debug_mode > 0):
            logits_np = results[0]
            self.cache_np= results[1]
            max_logits = np.max(logits_np, axis=1)[0]
            max_p = np.max(max_logits)
            idx = np.argmax(max_logits)
            # 如果分数大于阈值，且idx==1(即包含唤醒词)，播放回复音频
            if max_p > self.threshold:
                return idx
            else:
                return -1





class AudioApp(AIBase):
    def __init__(self, base_url=""):
        self.frames = []
        self.api_url = base_url
        self.CHUNK = 44100//25      #设置音频chunk值
        self.FORMAT = paInt16       #设置采样精度,支持16bit(paInt16)/24bit(paInt24)/32bit(paInt32)
        self.CHANNELS = 1           #设置声道数,支持单声道(1)/立体声(2)
        self.RATE = 44100

        pass
    def add_wav_frames(self, data):
        pass


    def play_base64_wav(self, p, base64_data="", filename=""):
        # 解码base64
        if not filename and base64_data:
            wav_data = base64.b64decode(base64_data)
            wav_buffer = io.BytesIO(wav_data)
        elif filename and not base64_data:
            wav_buffer = filename


        # 创建内存中的WAV文件
        with wave.open(wav_buffer, 'rb') as wav_file:
                # 打开音频流
                stream = p.open(format=p.get_format_from_width(wav_file.get_sampwidth()),
                            channels=wav_file.get_channels(),
                            rate=wav_file.get_framerate(),
                            output=True,frames_per_buffer=self.CHUNK)

                #设置音频输出流的音量
                stream.volume(vol=85)

                data = wav_file.read_frames(self.CHUNK)#从wav文件中读取数一帧数据

                while data:
                    stream.write(data)  #将帧数据写入到音频输出流中
                    data = wav_file.read_frames(self.CHUNK) #从wav文件中读取数一帧数据
                    if exit_check():
                        break

                # 清理资源
                stream.stop_stream()
                stream.close()


    def text2audio(self, text, filename = "tmp.wav"):
        CHUNK = 44100//25      #设置音频chunk值
        FORMAT = paInt16       #设置采样精度,支持16bit(paInt16)/24bit(paInt24)/32bit(paInt32)
        CHANNELS = 1           #设置声道数,支持单声道(1)/立体声(2)
        RATE = 44100           #设置采样率

        url = f"https://tsn.baidu.com/text2audio?"
        url +=f"tex={text}&lan=zh&cuid=wwk123&ctp=1&aue=6"
        url +="&tok=bce-v3/ALTAK-0yTWZeU4tmBZpjQgNEigh/07d55083d1a1af8fcf7c97e0607c5df5a55d2f17"
        url +='&audio_ctrl={"sampling_rate":16000}'

        response = requests.post(
            url,
            timeout=120  # 设置超时时间
        )

        # 发送POST请求
#        url= "https://tsn.baidu.com/text2audio"
        print("Sending to URL: ", url)
        print("Response Header: ", response.headers)
        print("Response: ", response.status_code)
        if response.status_code == 200:
            print(f"Successfully get data")
            data = response.content
            print("data: ", data)
        else:
            print(f"Failed to send images. Status code: {response.status_code}")
            data= None
        if data is not None and not isinstance(data, dict):
            print("Saving data to ", filename)
            with open(filename, "wb") as f:
                f.write(data)

            print("Audio saved")


    def request_server(self, frames=[], tot_bytes=0, output_stream=None):
        print("request server frames type: ", type(frames[0]))

#        chunk_bytes = 100000
        chunk_bytes = 50000
        num_chunks = tot_bytes//chunk_bytes + tot_bytes%chunk_bytes
        num_chunks = 2
        chunk_len = len(frames)//num_chunks + len(frames)%num_chunks

        cache = []
        chunks = []
        text = ""
        for idx, v in enumerate(frames):
            cache.append(v)
            if (idx!=0 and idx % chunk_len ==0) or idx == len(frames)-1:
                chunks.append( b"".join(cache) )
                cache.clear()
        print("tot_bytes=",tot_bytes,"chunks: ", len(chunks)," chunk_len: ",chunk_len, "p.get_sample_size(self.FORMAT) type: ", type(p.get_sample_size(self.FORMAT)))

        max_retry = 1
        chunks += [b""] *5
        for i, f in enumerate(chunks):
            print("Converting data")
            frame_bytes = bytes(f)
            bytes_size = len(frame_bytes)
            frame_base64 = ubinascii.b2a_base64(frame_bytes)#.decode().strip()
#            frame_base64 = base64.b64encode(frame_bytes).decode().strip() #这里会卡住
            retry = 0
            while retry < max_retry:
                try:
                    resp = self.chat_llm(audio_data=frame_base64,
                                         audio_format="bytes",
                                         audio_bytes_size=bytes_size,
                                         num_frames=len(chunks),
                                         frame_idx = i+1)

                    json_resp = resp.json()
                    if  ("success" in json_resp and str(json_resp.get("success","false")).lower() == 'true'
                        and  len(json_resp['message']) >0
                        ):
                        text += json_resp['message']
                        print("Text: ", text)
                        return text

                    # for i in range(5):
                    #     response = requests.post(
                    #         SERVER_URL,
                    #         timeout=10  # 设置超时时间
                    #     )
                    retry = max_retry
                except Exception as e:
                    retry += 1
                    print(f"chat_llm request Exception: {e}")
                    print(f"retry = {retry}/{max_retry}")
                    play_wave_audio("/sdcard/examples/utils/thinking_v2.wav", output_stream, CHUNK)
                    time.sleep(1.0)
            time.sleep(0.2)
        ## parse audio in server if need
        #resp = self.chat_llm(audio_data=frame_base64, audio_format="bytes", audio_bytes_size=bytes_size)
        #text_res = self.request_a2t(frame_base64, bytes_size, format_str='pcm')
        #resp = self.chat_llm(audio_data=text_res, audio_format="text", audio_bytes_size=0)

        return text


    def request_a2t(self, frames_str, bytes_size, format_str='pcm'):
        data={
            "format":format_str,
            "rate":16000,
            "dev_pid":1537,
            "channel":1,
            "token": "bce-v3/ALTAK-0yTWZeU4tmBZpjQgNEigh/07d55083d1a1af8fcf7c97e0607c5df5a55d2f17",
            "cuid":"wwk123",
            "len":bytes_size,
            "speech":frames_str
        }

#        url="http://vop.baidu.com/pro_api"
        url="http://vop.baidu.com/server_api"

        payload = ujson.dumps(data)
        if not isinstance(payload, str):
            payload = str(payload)
        headers = {
                    'Content-Type': 'application/json'
                }
        # 发送POST请求
        print("Sending to URL: ", url)

        response = requests.post(
            url,
            headers=headers,
#            data=payload,
            json=data,
            timeout=120  # 设置超时时间
        )
        print("Response: ", response.text)
        if response.status_code == 200:
            print(f"Successfully get response")
            res = response.text
            if "result" in res and res.get("err_msg", "") == "success":
                return res["result"]
        else:
            print(f"Failed to get result. Status code: {response.status_code}")
            return None

    def audio2text(self, filename="/sdcard/examples/tmp.wav", frames=[]):
        print("Start audio2text")


        with open(filename, 'rb') as fp:
            wave_byte = fp.read()
            bytes_size = len(wave_byte)
            wave_data =  base64.b64encode(wave_byte).decode('utf-8').strip()
        print("wave data = ", wave_data)

        return self.request_a2t(wave_data, bytes_size, format_str='wav')

    def chat_llm(self, url="", audio_data="", audio_format="text", audio_bytes_size=0, num_frames=0, frame_idx=0):

        # 添加其他元数据
        data = {
            'device_id': 'k210_camera',  # 可以修改为您的设备ID
            'timestamp': float(time.time()),
            'audio_bytes_size': audio_bytes_size,
            'audio_format': audio_format,
            "audio_data": audio_data,
            "num_frames": num_frames,
            "frame_idx": frame_idx,
            "channels": CHANNELS,
            "rate": RATE,
            "sample_size": p.get_sample_size(self.FORMAT)
        }
        payload = ujson.dumps(data)
        if not isinstance(payload, str):
            payload = str(payload)
        headers = {
                    'Content-Type': 'application/json',
                    'User-Agent': 'K230-Camera/1.0'
                }

        # 发送POST请求
        if not url:
            url = self.api_url
        url =url + "/chat_llm"
        print("Sending to URL: ", url)

        response = requests.post(
            url,
            headers=headers,
            data=payload,
            timeout=2000  # 设置超时时间
        )
        print("Response: ", response.text,  "response.status_code= ",response.status_code)
        if response.status_code == 200:
            print(f"Successfully sent chat request")
        else:
            print(f"Failed to send  chat request. Status code: {response.status_code}")

        return response


    def save_wav(self, frames, p, filename):
        #将列表中的数据保存到wav文件中
        wf = wave.open(filename, 'wb') #创建wav 文件
        wf.set_channels(self.CHANNELS) #设置wav 声道数
        wf.set_sampwidth(p.get_sample_size(self.FORMAT))  #设置wav 采样精度
        wf.set_framerate(self.RATE)  #设置wav 采样率
        wf.write_frames(b''.join(frames)) #存储wav音频数据
        wf.close() #关闭wav文件


def play_wave_audio(wave_path, output_stream, data_chunk):
    wf = wave.open(wave_path, "rb")
    wav_data = wf.read_frames(data_chunk)
    while wav_data:
        output_stream.write(wav_data)
        wav_data = wf.read_frames(data_chunk)
    time.sleep(2.5) # 时间缓冲，用于播放回复声音
    wf.close()



def audio_app():
    global pl, p, send_lock
    nn.shrink_memory_pool()
    duration = 5
    # filename = save_wav_file = "/sdcard/examples/test_audio_v1.wav"
    os.exitpoint(os.EXITPOINT_ENABLE)
    nn.shrink_memory_pool()
    # 设置模型路径和其他参数
    kmodel_path = "/sdcard/examples/kmodel/multi_kws.kmodel"
    kws = KWSApp(kmodel_path,threshold=THRESH,debug_mode=0)
    last_idx=0
    aapp = AudioApp(base_url=SERVER_URL)
    #创建音频输入流
    input_stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=SAMPLE_RATE,
                    input=True,
                    frames_per_buffer=CHUNK)
    output_stream = p.open(format=FORMAT,
                           channels=CHANNELS,
                           rate=SAMPLE_RATE,
                           output=True,
                           frames_per_buffer=CHUNK)

#    input_stream.volume(70, LEFT)
#    input_stream.volume(85, RIGHT)
    print("input volume :",input_stream.volume())

    #启用音频3A功能：自动噪声抑制(ANS)
    input_stream.enable_audio3a(AUDIO_3A_ENABLE_ANS)
    print("enable audio 3a:ans")

    # enter loop
#    aapp.text2audio("让小楠先想想呢","/sdcard/examples/utils/thinking_v2.wav")
#    aapp.text2audio("想不到呢,再问问","/sdcard/examples/utils/retry.wav")
    history = []
    try:
        while True:
            os.exitpoint()
            if audio_app_stop:
                print("audio_app_stop=True")
                break
#            print("Start AudioAPP")
            pcm_data=input_stream.read()
            res=kws.run(pcm_data)
            print("res = ", res)
            if last_idx!=1 and res==1:
                print("====Detected Go!====")
                play_wave_audio("/sdcard/examples/utils/go_new.wav", output_stream, CHUNK)
                # 开始录音
                record_duration = 5
                tot_bytes = 0
                for i in range(0, int(SAMPLE_RATE / CHUNK * record_duration)):
                    data = input_stream.read()
                    aapp.frames.append(data)
                    tot_bytes += len(bytes(data))
                print("====Requesting large model====")
                send_lock=True
                #with lock:
                with lock:

                    try:
                        audio_resp = aapp.request_server(aapp.frames, tot_bytes, output_stream)
                    except Exception as e:
                        print(f"Request large model Exception: {e}")


                try:

                    print("====Text to Audio====")
                    print("Converting text: ", audio_resp)

#                    aapp.text2audio("小楠没听清",generated_audio_file)
                    generated_audio_file = "/sdcard/examples/ai_audio.wav"
                    if len(audio_resp) > 0:
                        #清空 cache
#                        for i in range(10):
#                            response = requests.post(
#                                SERVER_URL,
#                                timeout=10  # 设置超时时间
#                            )
                        print("Generating audio =", generated_audio_file)
                        aapp.text2audio(audio_resp,generated_audio_file)
                    else:
                        generated_audio_file="/sdcard/examples/utils/retry.wav"
#                        generated_audio_file="/sdcard/examples/utils/not_clear.wav"

                    print("====Playing Generated Audio====")
                    play_wave_audio(generated_audio_file, output_stream, CHUNK)
                except Exception as e:
                    print(f"Request Text2Audio Exception: {e}")
                send_lock=False

            elif last_idx!=3 and res==3:
                print("====Detected Stop!====")
                play_wave_audio("/sdcard/examples/utils/stop_new.wav",output_stream, CHUNK)
            last_idx=res
            aapp.frames.clear()
            gc.collect()
#            print("END AudioAPP")
            if exit_check():
                aapp.frames.clear()
                print("exit_check ")
                break


    except BaseException as e:
            import sys
            sys.print_exception(e)
    finally:
            input_stream.stop_stream() #停止采集音频数据
            input_stream.close()#关闭音频输入流
            output_stream.stop_stream() #停止播放音频数据
            p.terminate() #释放音频对象
            # MediaManager.deinit() #释放vb buffer
            aidemo.kws_fp_destroy(fp)


class ObjectDetectionApp(AIBase):
    def __init__(self,kmodel_path,labels,model_input_size, max_boxes_num, base_url="", confidence_threshold=0.5,nms_threshold=0.2,rgb888p_size=[224,224],display_size=[1920,1080],debug_mode=0):
        super().__init__(kmodel_path,model_input_size,rgb888p_size,debug_mode)
        self.kmodel_path=kmodel_path
        self.labels=labels
        # 模型输入分辨率
        self.model_input_size=model_input_size
        # 阈值设置
        self.confidence_threshold=confidence_threshold
        self.nms_threshold=nms_threshold
        self.max_boxes_num=max_boxes_num
        # sensor给到AI的图像分辨率
        self.rgb888p_size=[ALIGN_UP(rgb888p_size[0],16),rgb888p_size[1]]
        # 显示分辨率
        self.display_size=[ALIGN_UP(display_size[0],16),display_size[1]]
        self.debug_mode=debug_mode
        # 检测框预置颜色值
        self.color_four=get_colors(len(self.labels))
        # 宽高缩放比例
        self.x_factor = float(self.rgb888p_size[0])/self.model_input_size[0]
        self.y_factor = float(self.rgb888p_size[1])/self.model_input_size[1]
        # Ai2d实例，用于实现模型预处理
        self.ai2d=Ai2d(debug_mode)
        # 设置Ai2d的输入输出格式和类型
        self.ai2d.set_ai2d_dtype(nn.ai2d_format.NCHW_FMT,nn.ai2d_format.NCHW_FMT,np.uint8, np.uint8)
        # 图像发送相关配置
        self.api_url = base_url  # 替换为您的API地址
        self.batch_size = 5  # 批量发送的帧数
        self.batch_counter = 0
        self.image_batch = []


    # 配置预处理操作，这里使用了resize，Ai2d支持crop/shift/pad/resize/affine，具体代码请打开/sdcard/app/libs/AI2D.py查看
    def config_preprocess(self,input_image_size=None):
        with ScopedTiming("set preprocess config",self.debug_mode > 0):
            # 初始化ai2d预处理配置，默认为sensor给到AI的尺寸，您可以通过设置input_image_size自行修改输入尺寸
            ai2d_input_size=input_image_size if input_image_size else self.rgb888p_size
            top,bottom,left,right,self.scale=letterbox_pad_param(self.rgb888p_size,self.model_input_size)
            # 配置padding预处理
            self.ai2d.pad([0,0,0,0,top,bottom,left,right], 0, [128,128,128])
            self.ai2d.resize(nn.interp_method.tf_bilinear, nn.interp_mode.half_pixel)
            self.ai2d.build([1,3,ai2d_input_size[1],ai2d_input_size[0]],[1,3,self.model_input_size[1],self.model_input_size[0]])

    def preprocess(self,input_np):
        with ScopedTiming("preprocess",self.debug_mode > 0):
            return [nn.from_numpy(input_np)]

    # 自定义当前任务的后处理
    def postprocess(self,results):
        with ScopedTiming("postprocess",self.debug_mode > 0):
            new_result=results[0][0].transpose()
            det_res = aidemo.yolov8_det_postprocess(new_result.copy(),[self.rgb888p_size[1],self.rgb888p_size[0]],[self.model_input_size[1],self.model_input_size[0]],[self.display_size[1],self.display_size[0]],len(self.labels),self.confidence_threshold,self.nms_threshold,self.max_boxes_num)
            return det_res

    # 绘制结果
    def draw_result(self,pl,dets):
        with ScopedTiming("display_draw",self.debug_mode >0):
            if dets:
                pl.osd_img.clear()
                for i in range(len(dets[0])):
                    x, y, w, h = map(lambda x: int(round(x, 0)), dets[0][i])
                    pl.osd_img.draw_rectangle(x,y, w, h, color=self.color_four[dets[1][i]],thickness=4)
                    pl.osd_img.draw_string_advanced( x , y-50,32," " + self.labels[dets[1][i]] + " " + str(round(dets[2][i],2)) , color=self.color_four[dets[1][i]])
                    return self.labels[dets[1][i]]
            else:
                pl.osd_img.clear()
                return None




    def ndarray_to_png_k210(self, image_array):
        """将 numpy ndarray 转换为 PNG 字节数据"""
        try:
            print(f"Debug: Array shape: {image_array.shape}")
            print(f"Debug: Array dtype: {image_array.dtype}")

            # 处理不正常的通道数
            if len(image_array.shape) == 3 and image_array.shape[2] > 4:
                # 如果是多通道数据（如320个通道），需要特殊处理
                print(f"Warning: Multi-channel image with {image_array.shape[2]} channels")

                # 方法1: 取前3个通道作为RGB
                if image_array.shape[2] >= 3:
                    rgb_array = image_array[:, :, :3]  # 取前3个通道
                    return self._convert_normal_image(rgb_array)

                # 方法2: 转换为灰度图
                else:
                    gray_array = np.mean(image_array, axis=2)  # 通道平均
                    return self._convert_normal_image(gray_array)

            else:
                # 正常图像处理
                return self._convert_normal_image(image_array)

        except Exception as e:
            print(f"Error in ndarray_to_png_k210: {e}")
            return None

    def _convert_normal_image(self, image_array):
        """处理正常图像格式的转换"""
        try:
            # 获取图像尺寸
            if len(image_array.shape) == 2:
                # 灰度图
                h, w = image_array.shape
                img_format = image.GRAYSCALE
            elif len(image_array.shape) == 3:
                # 彩色图
                h, w, channels = image_array.shape
                if channels == 1:
                    img_format = image.GRAYSCALE
                    image_array = image_array.reshape(h, w)  # 去除通道维度
                elif channels == 3:
                    img_format = image.RGB888
                elif channels == 4:
                    img_format = image.ARGB8888
                else:
                    raise ValueError(f"不支持的通道数: {channels}")
            else:
                raise ValueError(f"不支持的数组维度: {len(image_array.shape)}")

            # 确保数据类型正确
            #print("Checking np data type")
            if image_array.dtype != np.uint8:
                # 归一化并转换为uint8
                if image_array.max() > 1.0:  # 假设是0-255范围
                    image_array = image_array.astype(np.uint8)
                else:  # 假设是0-1浮点数
                    image_array = (image_array * 255).astype(np.uint8)

            #print("Checking Image object type")
            # 创建 image.Image 对象
            img_obj = image.Image(w, h, img_format, alloc=image.ALLOC_REF, data=image_array)
#            img_obj = image.Image(w, h, img_format, data=image_array)

            # 转换为 PNG
            print("converting PNG Image")
            return img_obj.to_png()

        except Exception as e:
            print(f"Error in _convert_normal_image: {e}")
            return None



    # 将图像转换为PNG格式并添加到批量队列
    def add_image_to_batch(self, img, label=None):
        try:
#            new_img = img.reshape( (320,320,3))
            new_img = img.reshape( ( img.shape[1], img.shape[2], img.shape[0]))
            print("new_img shape=", new_img.shape)
            png_data = self.ndarray_to_png_k210(new_img)
            image_time = time.time()
            self.image_batch.append([image_time, png_data, str(label)])
            self.batch_counter += 1

        except Exception as e:
            print(f"Error converting image to PNG: {e}")

    # 批量发送图像到远程API
    def send_image_batch(self, url ="", image_batch = None):
        if not image_batch:
            image_batch = self.image_batch
        if not image_batch:
            return
        if 1:
            # 准备多部分表单数据
            files = []
            print("Preparing data")
            for i, png_data in enumerate(image_batch):
                timestamp =png_data[0]
                image_bytes_data = png_data[1]
                label = png_data[2]
                image_d = bytes(image_bytes_data)
                image_base64 = ubinascii.b2a_base64(image_d).decode().strip()
                #timestamp = int(time.time() * 1000)
                files.append({
                    "timestamp":f'{timestamp}', "data":image_base64, "label": str(label)
                })

#                print("send label:", str(label))
            # 添加其他元数据
            data = {
                'device_id': 'k210_camera',  # 可以修改为您的设备ID
                'filename': "k210_camera.png",
                'timestamp': float(time.time()),
                'total_images': len(self.image_batch),
                'image_format': "png_base64",
                "image_data": files
            }
            payload = ujson.dumps(data)
            if not isinstance(payload, str):
                payload = str(payload)
            headers = {
                        'Content-Type': 'application/json',
                        'User-Agent': 'K230-Camera/1.0'
                    }
            # 发送POST请求
            if not url:
                url = self.api_url
            url =url + "/get_images_v1"
            print("Sending to URL: ", url)
            #                files=files,

            response = requests.post(
                url,
                headers=headers,
                data=payload,
                timeout=120  # 设置超时时间
            )
            print("Response: ", response.text)
            if response.status_code == 200:
                print(f"Successfully sent batch of {len(self.image_batch)} images")
            else:
                print(f"Failed to send images. Status code: {response.status_code}")

    # 析构函数，确保最后一批图像也被发送
    def __del__(self):
        if self.image_batch:
            self.send_image_batch()


def vision_app():
    # ==============================initialize network
    global pl, p, send_lock
    # initialization
    display_mode="hdmi"
    rgb888p_size=[224,224]
    # 模型路径
    kmodel_path="/sdcard/examples/kmodel/yolov8n_224.kmodel"
    labels = ["person", "bicycle", "car", "motorcycle", "airplane", "bus", "train", "truck", "boat", "traffic light", "fire hydrant", "stop sign", "parking meter", "bench", "bird", "cat", "dog", "horse", "sheep", "cow", "elephant", "bear", "zebra", "giraffe", "backpack", "umbrella", "handbag", "tie", "suitcase", "frisbee", "skis", "snowboard", "sports ball", "kite", "baseball bat", "baseball glove", "skateboard", "surfboard", "tennis racket", "bottle", "wine glass", "cup", "fork", "knife", "spoon", "bowl", "banana", "apple", "sandwich", "orange", "broccoli", "carrot", "hot dog", "pizza", "donut", "cake", "chair", "couch", "potted plant", "bed", "dining table", "toilet", "tv", "laptop", "mouse", "remote", "keyboard", "cell phone", "microwave", "oven", "toaster", "sink", "refrigerator", "book", "clock", "vase", "scissors", "teddy bear", "hair drier", "toothbrush"]
    # 其它参数设置
    confidence_threshold = 0.3
    nms_threshold = 0.4
    max_boxes_num = 30
    # 初始化PipeLine
    display_size=pl.get_display_size()


    seg=ObjectDetectionApp(kmodel_path,labels=labels,model_input_size=[224,224],
                           max_boxes_num=max_boxes_num,
                           confidence_threshold=confidence_threshold,
                           nms_threshold=nms_threshold,rgb888p_size=rgb888p_size,
                           display_size=display_size,debug_mode=0,base_url=SERVER_URL)
    seg.config_preprocess()

    max_retry=3
    cnt=0
    # image loop
    try:
        start_time = time.time()
        while True:
            if vision_app_stop:
                break
            try:
                with ScopedTiming("total",1):
                    with lock:
                        # 获取当前帧数据
                        img=pl.get_frame()
                        # 推理当前帧
                        seg_res=seg.run(img)

                    # 绘制结果到PipeLine的osd图像
                    label = seg.draw_result(pl,seg_res)
                    print("Label: ", label)

                    # 将图像添加到批量发送队列
                    seg.add_image_to_batch(img, label)
                    # 显示当前的绘制结果
                    pl.show_image()
#                    time.sleep(0.5)
                    time.sleep(0.2)
                    end_time = time.time()
                    elapsed_time = end_time - start_time

                    if elapsed_time>=3 and not send_lock:
                        print("Time elapsed(s): ", elapsed_time)
                        start_time = end_time
                        print("Sending images size = ", len(seg.image_batch))
                        if hasattr(seg, 'image_batch') and seg.image_batch :

                            seg.send_image_batch()
                    seg.image_batch.clear()

            except Exception as e:
                cnt += 1
                print(f"Exception: {e}, retry = {cnt}/{max_retry}")
                if cnt > max_retry:
                    break

            gc.collect()

    except KeyboardInterrupt:
        print("Program interrupted by user")
    finally:
        # 确保最后一批图像被发送
        seg.deinit()
        pl.destroy()

def media_init():
    global pl, p
    # initialization
    # yolo detection



vision_app_stop=False
audio_app_stop=False

if __name__=="__main__":

    os.exitpoint(os.EXITPOINT_ENABLE)
    network_use_wlan(True)
    media_init()
    _thread.start_new_thread(vision_app,())
#    _thread.start_new_thread(audio_app,())
    try:
        while True:
            time.sleep_ms(50)
    except BaseException as e:
        import sys
        sys.print_exception(e)
        vision_app_stop=True
        audio_app_stop=True
    time.sleep(1)
    gc.collect()




