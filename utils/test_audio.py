# # from modelscope.outputs import OutputKeys
# # from modelscope.pipelines import pipeline
# # from modelscope.utils.constant import Tasks

# # # 使用魔搭社区提供的 pipeline，非常简单
# # # 将 'damo/speech_sambert-hifigan_tts_zh-cn_16k' 替换成你在魔搭上找到的最新模型名称
# # model_id = 'damo/speech_sambert-hifigan_tts_zh-cn_16k'
# # tts_pipeline = pipeline(task=Tasks.text_to_speech, model=model_id)

# # # 输入文本和发音人参数
# # input_text = "春风送暖，万象更新。" 
# # output = tts_pipeline(input_text, voice='zhitian_emo')

# # # 保存音频
# # wav = output[OutputKeys.OUTPUT_WAVEFORM]
# # with open('output_ns3.wav', 'wb') as f:
# #     f.write(wav)

# # print("NaturalSpeech 3 语音合成完成！")



# # # from transformers import AutoModel, AutoProcessor
# # # import soundfile as sf
# # # import os
# # # # 指定模型名称 (使用国内镜像站上的模型，例如 modelscope)
# # # model_name = "tts_models/zh-CN/baker/fastspeech2"
# # # os.environ['HF_ENDPOINT'] = 'https://hf-mirror.com'
# # # # 如果您无法直接下载，可以先去 https://www.modelscope.cn/models 搜索 "fastspeech2" 找到模型，然后通过git lfs下载到本地
# # # # 然后使用本地路径：model_name = "/your/local/path/to/fastspeech2-model"

# # # # 加载处理器和模型
# # # processor = AutoProcessor.from_pretrained(model_name, trust_remote_code=True)
# # # model = AutoModel.from_pretrained(model_name, trust_remote_code=True)

# # # # 输入文本
# # # text = "大家好，这是一个测试语音合成的例子。"

# # # # 处理文本并生成语音
# # # inputs = processor(text=text, return_tensors="pt")
# # # with torch.no_grad():
# # #     output = model(**inputs)

# # # # 保存音频文件
# # # audio = output.waveform.squeeze().numpy()
# # # sample_rate = output.sample_rate
# # # sf.write("output.wav", audio, sample_rate)

# # # print("语音合成完成，已保存到 output.wav")


# from modelscope.pipelines import pipeline
# from modelscope.utils.constant import Tasks
# import soundfile as sf

# # 使用其他可用的TTS模型
# def use_alternative_tts_model():
#     # 尝试其他中文TTS模型
#     alternative_models = [
#         'damo/speech_sambert-hifigan_tts_zhitian_emo_zh-cn_16k',
#         'damo/speech_sambert-hifigan_tts_zhiyan_emo_zh-cn_16k',
#         'damo/speech_sambert-hifigan_tts_zhizhe_emo_zh-cn_16k',
#         'damo/speech_sambert-hifigan_tts_zh-cn_16k'  # 原始模型
#     ]
    
#     for model_name in alternative_models:
#         try:
#             print(f"尝试使用模型: {model_name}")
#             tts_pipeline = pipeline(
#                 task=Tasks.text_to_speech,
#                 model=model_name
#             )
            
#             result = tts_pipeline("测试文本", voice="default")
#             sf.write("output.wav", result['output_wav'], result['sample_rate'])
#             print(f"成功使用模型: {model_name}")
#             return tts_pipeline
            
#         except Exception as e:
#             print(f"模型 {model_name} 失败: {e}")
#             continue
    
#     return None

# # 使用示例
# tts_pipeline = use_alternative_tts_model()
# if tts_pipeline:
#     result = tts_pipeline("你好，这是一个测试", voice="zhizhe_emo")
#     sf.write("output.wav", result['output_wav'], result['sample_rate'])


from modelscope.hub.snapshot_download import snapshot_download
from modelscope.models import Model
import torch
import soundfile as sf

def simple_tts_workaround(text, output_file="output.wav"):
    """使用简化的TTS工作区"""
    try:
        # 直接下载模型
        model_dir = snapshot_download('damo/speech_sambert-hifigan_tts_zh-cn_16k')
        print(f"模型下载到: {model_dir}")
        
        # 尝试直接加载模型
        model = Model.from_pretrained(model_dir)
        
        # 使用模型的forward方法（如果可用）
        if hasattr(model, 'forward'):
            # 这里需要根据具体模型调整输入格式
            result = model.forward(text)
            sf.write(output_file, result, 16000)
            return output_file
            
    except Exception as e:
        print(f"简化方法失败: {e}")
        return None

# 使用示例
simple_tts_workaround("测试文本")
