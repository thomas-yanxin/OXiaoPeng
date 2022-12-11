# import wenxin_api  # 可以通过"pip install wenxin-api"命令安装
# from wenxin_api.tasks.free_qa import FreeQA

# wenxin_api.ak = "8eSZX6kEG7FFTruEGFQ8IUkRRZbGSMqg"
# wenxin_api.sk = "47jlwtACeGLZ5sM5HGemqsx70Oo1LT3h"
# input_dict = {
#     "text": "问题：做生意的基本原则是什么？\n回答：",
#     "seq_len": 512,
#     "topp": 0.5,
#     "penalty_score": 1.2,
#     "min_dec_len": 2,
#     "min_dec_penalty_text": "。?：！",
#     "is_unidirectional": 0,
#     "task_prompt": "qa",
#     "mask_type": "word"
# }
# rst = FreeQA.create(**input_dict)
# print(rst['result'])


import json

import requests

texts =["今天是个好日子"]
data = {"data": texts}
# 发送post请求，content-type类型应指定json方式，url中的ip地址需改为对应机器的ip
url = "http://127.0.0.1:8866/predict/unified_transformer_12L_cn_luge"
# 指定post请求的headers为application/json方式
headers = {"Content-Type": "application/json"}

r = requests.post(url=url, headers=headers, data=json.dumps(data))
print(r.json()['results'])
