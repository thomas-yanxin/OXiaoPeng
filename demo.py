# -*- coding: utf-8 -*-
import sys
import time
import xml.dom.minidom
from tkinter import image_names

import ntchat
import requests
import wenxin_api  # 可以通过"pip install wenxin-api"命令安装
from pcl_pangu.online import Infer
from wenxin_api.tasks.text_to_image import TextToImage

model = "pangu-alpha-evolution-2B6-pt"

# 请填写api_key
# 获取方式见：https://git.openi.org.cn/PCL-Platform.Intelligence/pcl_pangu/src/branch/master/docs/api_key%E8%8E%B7%E5%8F%96%E6%8C%87%E5%8D%97.doc
pangu_api_key = '***************************************'

# 群聊的wxid
room_wxid = '********************'


wechat = ntchat.WeChat()

# 打开pc微信, smart: 是否管理已经登录的微信
wechat.open(smart=True)

# 等待登录
wechat.wait_login()

# # 获取联系人列表并输出
# contacts = wechat.get_contacts()

# print("联系人列表: ")
# print(contacts)

rooms = wechat.get_rooms()

print("群列表: ")

# print(rooms)
myself_wxid = wechat.get_self_info()['wxid']
print(wechat.get_self_info())
print(myself_wxid)

# 注册消息回调
@wechat.msg_register(ntchat.MT_RECV_FRIEND_MSG)
def on_recv_text_msg(wechat_instance: ntchat.WeChat, message):
    xml_content = message["data"]["raw_msg"]
    dom = xml.dom.minidom.parseString(xml_content)

    # 从xml取相关参数
    encryptusername = dom.documentElement.getAttribute("encryptusername")

    ticket = dom.documentElement.getAttribute("ticket")

    scene = dom.documentElement.getAttribute("scene")
    from_wxid = message['data']['from_wxid']
    
    # 自动同意好友申请
    wechat_instance.accept_friend_request(encryptusername, ticket, int(scene))

    wechat_instance.send_text(to_wxid=from_wxid, content=f"您好~我是OpenI小助手。\n\n您可以回复【加群】加入OpenI官方社区。\n\n回复【盘古+input】可体验鹏城·盘古α大模型生成能力。如：“盘古 中国和美国和日本和法国和加拿大和澳大利亚的首都分别是哪里？”\n\n回复【文心+风格+prompt】可体验ERNIE-ViLG的AIGC图文生成能力（目前支持“水彩”、“油画”、“粉笔画”、“卡通”、“蜡笔画”、“儿童画”、“探索无限”七种风格），如“文心 油画 睡莲”")

# 注册消息回调
@wechat.msg_register(ntchat.MT_RECV_TEXT_MSG)
def on_recv_text_msg(wechat_instance: ntchat.WeChat, message):
    data = message["data"]

    from_wxid = data["from_wxid"]

    self_wxid = wechat_instance.get_login_info()["wxid"]

    room_wxid = data["room_wxid"]

    # 判断消息不是自己发的并且不是群消息时，回复对方
    if from_wxid != self_wxid and not room_wxid :
        if data["msg"] == '加群':

            wechat_instance.send_text(to_wxid=from_wxid, content=f"启智社区（简称OpenI）是在国家实施新一代人工智能发展战略背景下，新一代人工智能产业技术创新战略联盟（AITISA）组织产学研用协作共建共享的开源平台与社区，以鹏城云脑科学装置及Trustie软件开发群体化方法为基础，全面推动人工智能领域的开源开放与协同创新。社区在“开源开放、尊重创新”的原则下，汇聚学术界、产业界及社会其他各界力量，努力建设成具有国际影响力的人工智能开源开放平台与社区。")

            time.sleep(3)

            wechat_instance.send_text(to_wxid=from_wxid, content=f"入群后，您可以和启智社区的开发者进行交流。若您在使用中有任何问题，您可以在群内提出，提问格式可参考：\n 1. 问题描述:\n2. 相关环境：GPU / NPU\n3. 相关集群：启智/智算\n4. 任务名：\n5. 问题截图or log：")

            member = []

            member.append(data['from_wxid'])

            time.sleep(1)

            wechat_instance.add_room_member(room_wxid=room_wxid, member_list=member)

            time.sleep(1)

            wechat_instance.send_room_at_msg(to_wxid=room_wxid, content="{$@},欢迎加入启智社区！", at_list=member)

        elif data["msg"].split(' ')[0] == '盘古' :

            prompt_input = data["msg"].split(' ')[1]
            
            result = Infer.generate(model, prompt_input, api_key=pangu_api_key)  # api_key获取请见上文

            wechat_instance.send_text(to_wxid=from_wxid, content=result['results']['generate_text'])


        elif data["msg"].split(' ')[0] == '文心' :

            wechat_instance.send_text(to_wxid=from_wxid, content=f"请您稍等，图像正在生成中，大约需要1min~")

            import paddlehub as hub

            module = hub.Module(name="ernie_vilg")

            style_input = data['msg'].split(' ')[1]
            text_prompts = data["msg"].split(' ')[2]

            images = module.generate_image(text_prompts=text_prompts, style=style_input,  output_dir='./ernie_vilg_out/')  

            for i in range(5):

                time.sleep(0.5)
                image_path = '.\\ernie_vilg_out\\'+ data['msg'].split(' ')[2] + '_{}.png'.format(i)
                wechat_instance.send_image(to_wxid=from_wxid, file_path=image_path)

            time.sleep(5)
            wechat_instance.send_text(to_wxid=from_wxid, content=f"图像已生成完毕，希望您能喜欢~")

        else :
            wechat_instance.send_text(to_wxid=from_wxid, content=f'您好~我是OpenI小助手。\n\n1. 回复【加群】可以加入OpenI官方社区。\n\n2. 回复【盘古+input】可体验鹏城·盘古α大模型生成能力。\n如：“盘古 中国和美国和日本和法国和加拿大和澳大利亚的首都分别是哪里？”\n\n3. 回复【文心+风格+prompt】可体验ERNIE-ViLG的AIGC图文生成能力（目前仅支持“水彩”、“油画”、“粉笔画”、“卡通”、“蜡笔画”、“儿童画”、“探索无限”七种风格）。\n如“文心 油画 睡莲”。\n\n其他隐藏功能可自行探索。')

    elif from_wxid != self_wxid and  room_wxid :

        if from_wxid != self_wxid and myself_wxid in data['at_user_list']:

            text = data['msg'].split('\u2005')[1]
            
            result = Infer.generate(model, text, api_key=pangu_api_key)  # api_key获取请见上文

            wechat_instance.send_text(to_wxid=room_wxid, content=result['results']['generate_text'])


# 以下是为了让程序不结束，如果有用于PyQt等有主循环消息的框架，可以去除下面代码
try:
    while True:
        time.sleep(0.5)
except KeyboardInterrupt:
    ntchat.exit_()
    sys.exit()
