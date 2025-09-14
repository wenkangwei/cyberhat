#!/bin/bash
mode=''

[ -n $1 ] && mode=$1

# cd /home/wwk/workspace/ai_project/BookMonster/utils
# 将图片转为 Base64
# IMAGE_BASE64=$(base64 -i ../data/charactor/pikaqiu/pikaqiu.png  | tr -d '\n')

# curl  http://localhost:11434/api/generate  -d '{"prompt": "你好, 你猜猜图片里面是谁", "model": "qwen2.5-vl:7b", "stream": false, "image":["'"$IMAGE_BASE64"'"]}' 



# test agent model
# 本地图片路径和提示词
IMAGE_PATH="/home/wwk/workspace/ai_project/BookMonster/data/character/images/pikaqiu.png"
PROMPT="${IMAGE_PATH} 你好, 你猜猜图片里面是谁"
# IMAGE_BASE64=$(base64 -i $IMAGE_PATH  | tr -d '\n')

# curl http://0.0.0.0:8000/api/generate_bookmonster
echo "curl -X POST http://localhost:11434/api/generate -d '{"prompt": "'"$PROMPT"'", "model": "qwen2.5-vl:7b", "stream": false}'"
curl -X POST http://localhost:11434/api/generate -d '{"prompt": ${PROMPT}, "model": "qwen2.5-vl:7b", "stream": false}'


# IMAGE_BASE64=$(base64 -i image.jpg | tr -d '\n')

# curl -X POST "http://localhost:8000/api/generate_bookmonster" \
#   -H "Content-Type: application/json" \
#   -d "$(jq -n \
#     --arg prompt "描述这张图片" \
#     --arg model "qwen2.5-vl:7b" \
#     --arg image "$IMAGE_BASE64" \
#     '{
#       prompt: $prompt,
#       model: $model,
#       images: [$image]
#     }')"





# curl http://localhost:11434/api/generate -d @vl_model_req.json

# curl http://localhost:11434/api/generate -d @chat_model_req.json


# curl -X POST http://localhost:8000/api/debug -H "Content-Type: application/json" -d @vl_model_req.json

# curl -X POST http://localhost:8000/generate_bookmonster -H "Content-Type: application/json" -d @vl_model_req.json

# curl -X POST http://localhost:8000/enemy_action -H "Content-Type: application/json" -d @chat_model_req.json


# curl -X POST http://localhost:11434/api/embeddings -H "Content-Type: application/json" -d @vl_model_req.json





# curl -X POST http://localhost:8000/get_database_list \
#   -H "Content-Type: application/json" \
#   -d '{
#     "book_id":"640507"
#   }'



# curl -X POST http://localhost:8000/get_card_list \
#   -H "Content-Type: application/json" \
#   -d '{
#     "book_id":"640507"
#   }'

# if [ $mode == 1 ];then
# curl -X POST http://localhost:8000/get_database_list \
#   -H "Content-Type: application/json" \
#   -d '{
#     "book_id":"640507"
#   }'
# elif [ $mode == 2 ];then
# curl -X POST http://localhost:8000/get_card_list \
#   -H "Content-Type: application/json" \
#   -d '{
#     "book_id":"995975"
#   }'

# elif [ $mode == 3 ];then
# curl -X POST http://localhost:8000/delete_books_list \
#   -H "Content-Type: application/json" \
#   -d '{
#     "indices": ["284938","647931", "48602", "mmoe.pdf", "66965", "915769", "995975"]
#   }'
# elif [ $mode == 4 ];then
#     curl -X POST http://localhost:8000/chat \
#     -H "Content-Type: application/json" \
#     -d '{
#         "pdf_path": "/home/wwk/workspace/ai_project/BookMonster/data/upload/MMOE_paper.pdf",
#         "image_path": "/home/wwk/workspace/ai_project/BookMonster/data/upload/image_1755920536461.jpg",
#         "prompt": "请分析这个文档并提取关键信息生成知识卡片"
#     }'
# elif [ $mode == 5 ];then
# curl -X POST http://localhost:8000/chat \
#     -H "Content-Type: application/json" \
#     -d '{
#         "pdf_path": "",
#         "image_path": "",
#         "prompt": "请调用天气API来看看今天北京天气怎么样"
#     }'

# elif [ $mode == 6 ];then
# curl -X POST http://localhost:8000/chat \
#     -H "Content-Type: application/json" \
#     -d '{
#         "pdf_path": "",
#         "image_path": "",
#         "prompt": "请调用邮件API 发送邮件到1904832812@qq.com 邮箱， boday是”Hello world"
#     }'

# elif [ $mode == 7 ];then
# curl -X POST http://localhost:8000/get_card_recom \
#   -H "Content-Type: application/json" \
#   -d '{
#     "key":"personal_recom"
#     }'
# elif [ $mode == 8 ];then
# url="https://d5488ea6e17c.ngrok-free.app"
# curl -X POST $url/get_database_list \
#   -H "Content-Type: application/json" \
#   -d '{
#     "book_id":"640507"
#   }'

# fi


# curl -X POST  
# -H "Content-Type: application/json"
# -d ''



# curl -X POST https://65d9dbc34e5b.ngrok-free.app/chat_v2 \
#   -F "pdf_path=@/home/wwk/workspace/ai_project/KnowledgeMaster/front-end-react-v3/public/uploads/spectral-based-graph-neural-networks_v2.pdf" \
#   -F "image_path=@/home/wwk/workspace/ai_project/KnowledgeMaster/front-end-react-v3/public/uploads/book_example.jpg" \
#   -F "prompt=exciting rock indian music"
#  请求embedding向量测试
# curl http://localhost:11434/api/embeddings \
#     -X POST \
#     -H "Content-Type: application/json" \
#     -d '{
#       "model": "nomic-embed-text:latest",
#       "prompt": "The quick brown fox jumps over the lazy dog",
#       "options": {
#         "temperature": 0.7,
#         "top_p": 0.9
#       }
#     }'

#  {'model': 'qwen2.5vl:7b', 'created_at': '2025-08-02T09:29:27.72935443Z', 'response': '```json\n{\n    "maxHp": "10",\n    "skill": [\n        {\n            "question": "pikaqiu的主人叫什么名字？",\n            "answer1": "小k",\n            "answer2": "小明",\n            "answer3": "小红",\n            "correct_answer": "小k"\n        },\n        {\n            "question": "pikaqiu喜欢看的书籍是哪一本？",\n            "answer1": "钢铁就是力量",\n            "answer2": "哈利波特",\n            "answer3": "西游记",\n            "correct_answer": "钢铁就是力量"\n        },\n        {\n            "question": "pikaqiu的属性是什么？",\n            "answer1": "雷属性",\n            "answer2": "草属性",\n            "answer3": "冰属性",\n            "correct_answer": "雷属性"\n        },\n        {\n            "question": "pikaqiu的主人是算法工程师吗？",\n            "answer1": "是",\n            "answer2": "否",\n            "answer3": "不知道",\n            "correct_answer": "是"\n        }\n    ],\n    "attribute": "雷属性",\n    "name": "pikaqiu",\n    "level": "5",\n    "monster_image": "/home/wwk/workspace/ai_project/BookMonster/data/charactor/pikaqiu/pikaqiu.png"\n}\n```', 'done': True, 'done_reason': 'stop', 'context': [151644, 8948, 198, 2610, 525, 264, 10950, 17847, 13, 151645, 198, 151644, 872, 271, 18215, 14, 1250, 74, 93381, 14, 2143, 16352, 14, 7134, 50751, 13167, 14, 1762, 5621, 4322, 11496, 80, 18738, 4322, 11496, 80, 18738, 3508, 220, 56568, 101909, 104715, 2190, 17651, 43959, 31548, 3837, 103929, 88802, 20412, 100345, 110782, 82025, 57191, 16744, 37474, 29833, 8, 33108, 32664, 31196, 45930, 108894, 43959, 103124, 103936, 44177, 33108, 110019, 102349, 109487, 44177, 11, 90919, 102349, 109487, 101097, 18830, 19, 38989, 101043, 16, 38989, 88991, 3837, 106249, 2190, 50519, 107232, 44956, 8997, 101882, 5122, 112735, 11622, 99487, 100032, 44956, 43959, 46944, 2190, 50519, 100780, 3837, 54955, 240, 38035, 27369, 100630, 104121, 606, 3837, 3294, 3837, 29454, 11, 7035, 3837, 1932, 58363, 3837, 74577, 114, 100136, 23031, 2236, 68805, 31526, 3837, 86009, 30534, 104787, 115916, 104597, 198, 3294, 25, 103124, 86119, 9370, 104529, 104108, 18493, 16, 12, 16, 15, 101920, 3837, 16, 51463, 31235, 100405, 3837, 16, 15, 51463, 116080, 8997, 29454, 25, 69162, 50511, 100032, 44956, 103936, 9370, 31905, 3837, 54851, 46944, 2236, 9370, 1607, 3837, 6567, 107, 237, 18947, 102268, 101909, 2236, 64429, 3837, 94305, 227, 95312, 7841, 33108, 9217, 100369, 44931, 3837, 3405, 20412, 86119, 3837, 4226, 20412, 102349, 8997, 9116, 25, 69162, 50511, 109088, 9370, 79256, 3837, 79621, 59139, 100630, 8908, 235, 231, 79256, 3837, 96465, 79256, 3837, 100038, 79256, 3837, 79599, 79256, 3837, 113513, 79256, 198, 2810, 58363, 25, 103124, 109088, 100032, 44956, 100420, 86119, 9370, 38989, 8863, 3837, 60596, 94, 8863, 104108, 18493, 16, 12, 16, 15, 101920, 3837, 16, 51463, 31235, 100405, 3837, 16, 15, 51463, 116080, 3407, 112918, 20002, 34859, 31196, 105427, 28311, 2102, 25, 281, 11496, 80, 18738, 198, 4684, 25, 281, 11496, 80, 18738, 9370, 79256, 20412, 96465, 79256, 100631, 104963, 79256, 3837, 99729, 50930, 9370, 107041, 20412, 104706, 99486, 101102, 3837, 104121, 102543, 99882, 30709, 74, 104104, 107018, 105503, 198, 40581, 25, 608, 5117, 14, 1250, 74, 93381, 14, 2143, 16352, 14, 7134, 50751, 13167, 14, 1762, 5621, 4322, 11496, 80, 18738, 4322, 11496, 80, 18738, 3508, 220, 43959, 31905, 100420, 45930, 102073, 109088, 100780, 3837, 104040, 30534, 101266, 1022, 104314, 46944, 66017, 68805, 103358, 3837, 220, 14880, 99360, 100431, 9370, 2236, 104597, 107354, 16872, 116893, 101275, 104135, 20002, 31196, 104597, 43959, 9370, 105787, 100780, 104597, 3837, 220, 105182, 99360, 29454, 198, 100420, 103991, 7841, 30534, 43959, 110019, 19, 38989, 9217, 3837, 4226, 100420, 101043, 108075, 105045, 3837, 34369, 114, 42411, 100146, 32100, 9370, 1773, 105045, 9217, 9370, 792, 105792, 4396, 28534, 198, 341, 286, 330, 2810, 58363, 788, 330, 16, 15, 756, 286, 330, 29454, 788, 18396, 310, 330, 7841, 788, 8324, 310, 330, 9217, 16, 788, 8324, 310, 330, 9217, 17, 788, 8324, 310, 330, 9217, 18, 788, 8324, 310, 330, 19928, 28534, 788, 8324, 286, 29043, 286, 330, 9116, 788, 8324, 286, 330, 606, 788, 8324, 286, 330, 3294, 788, 8389, 286, 330, 50519, 4954, 788, 366, 1805, 2638, 397, 532, 151645, 198, 151644, 77091, 198, 73594, 2236, 198, 515, 262, 330, 2810, 58363, 788, 330, 16, 15, 756, 262, 330, 29454, 788, 2278, 286, 341, 310, 330, 7841, 788, 330, 79, 11496, 80, 18738, 9370, 102543, 99882, 99245, 101419, 11319, 756, 310, 330, 9217, 16, 788, 330, 30709, 74, 756, 310, 330, 9217, 17, 788, 330, 30709, 30858, 756, 310, 330, 9217, 18, 788, 330, 30709, 99425, 756, 310, 330, 19928, 28534, 788, 330, 30709, 74, 698, 286, 1153, 286, 341, 310, 330, 7841, 788, 330, 79, 11496, 80, 18738, 99729, 50930, 9370, 107041, 20412, 99459, 105663, 11319, 756, 310, 330, 9217, 16, 788, 330, 104706, 99486, 101102, 756, 310, 330, 9217, 17, 788, 330, 112597, 117731, 756, 310, 330, 9217, 18, 788, 330, 60686, 82894, 40814, 756, 310, 330, 19928, 28534, 788, 330, 104706, 99486, 101102, 698, 286, 1153, 286, 341, 310, 330, 7841, 788, 330, 79, 11496, 80, 18738, 9370, 79256, 102021, 11319, 756, 310, 330, 9217, 16, 788, 330, 96465, 79256, 756, 310, 330, 9217, 17, 788, 330, 99808, 79256, 756, 310, 330, 9217, 18, 788, 330, 100038, 79256, 756, 310, 330, 19928, 28534, 788, 330, 96465, 79256, 698, 286, 1153, 286, 341, 310, 330, 7841, 788, 330, 79, 11496, 80, 18738, 9370, 102543, 20412, 107018, 105503, 101037, 11319, 756, 310, 330, 9217, 16, 788, 330, 20412, 756, 310, 330, 9217, 17, 788, 330, 32376, 756, 310, 330, 9217, 18, 788, 330, 103950, 756, 310, 330, 19928, 28534, 788, 330, 20412, 698, 286, 456, 262, 3211, 262, 330, 9116, 788, 330, 96465, 79256, 756, 262, 330, 606, 788, 330, 79, 11496, 80, 18738, 756, 262, 330, 3294, 788, 330, 20, 756, 262, 330, 50519, 4954, 788, 3521, 5117, 14, 1250, 74, 93381, 14, 2143, 16352, 14, 7134, 50751, 13167, 14, 1762, 5621, 4322, 11496, 80, 18738, 4322, 11496, 80, 18738, 3508, 698, 532, 73594], 'total_duration': 12320404351, 'load_duration': 23291616, 'prompt_eval_count': 489, 'prompt_eval_duration': 268220536, 'eval_count': 303, 'eval_duration': 12028086283}


curl http://localhost:11434/api/generate \
    -X POST \
    -H "Content-Type: application/json" \
    -d '{
      "model": "qwen2.5vl:7b",
      "prompt": "The quick brown fox jumps over the lazy dog",
      "options": {
        "temperature": 0.7,
        "top_p": 0.9
      }
      "stream": False
    }'