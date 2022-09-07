# -*- coding: utf-8 -*-
import sys
import time
import xml.dom.minidom
from tkinter import image_names

import ntchat
import paddlehub as hub
import requests
import wenxin_api  # 可以通过"pip install wenxin-api"命令安装
from paddlenlp import Taskflow
from pcl_pangu.online import Infer
from wenxin_api.tasks.text_to_image import TextToImage

pangu_api_key = '**********************************'

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

    wechat_instance.send_text(to_wxid=from_wxid, content=f"您好~我是OpenI启智小助手。\n\n您可以回复【加群】加入OpenI官方社区（其实是本产品体验群）。\n\n回复【盘古+input】可体验鹏城·盘古α大模型生成能力。如：“盘古 中国和美国和日本和法国和加拿大和澳大利亚的首都分别是哪里？”\n\n回复【文心+风格+prompt】可体验ERNIE-ViLG的AIGC图文生成能力（目前支持“水彩”、“油画”、“粉笔画”、“卡通”、“蜡笔画”、“儿童画”、“探索无限”七种风格），如“文心 油画 睡莲”")



# 注册消息回调
@wechat.msg_register(ntchat.MT_RECV_TEXT_MSG)
def on_recv_text_msg(wechat_instance: ntchat.WeChat, message):
    data = message["data"]

    from_wxid = data["from_wxid"]

    self_wxid = wechat_instance.get_login_info()["wxid"]

    room_wxid = data["room_wxid"]


    # 判断消息不是自己发的并且不是群消息时，回复对方
    # 私信

    if from_wxid != self_wxid and not room_wxid :

        if data["msg"] == '加群':

            member = []
            member.append(data['from_wxid'])
            room_wxid = '*****************'
            # room_member_list = wechat.get_room_members(room_wxid='35045241311@chatroom')['member_list']

            # member_list = []

            # for i in room_member_list:
            #     member_list.append(i['wxid'])

            # print('群成员列表')
            # print(member_list)

            # if data['from_wxid'] in member_list:
            #     wechat_instance.send_text(to_wxid=from_wxid, content=f"您已在群中。")

            # else:
            wechat_instance.send_text(to_wxid=from_wxid, content=f"启智社区（简称OpenI）是在国家实施新一代人工智能发展战略背景下，新一代人工智能产业技术创新战略联盟（AITISA）组织产学研用协作共建共享的开源平台与社区，以鹏城云脑科学装置及Trustie软件开发群体化方法为基础，全面推动人工智能领域的开源开放与协同创新。社区在“开源开放、尊重创新”的原则下，汇聚学术界、产业界及社会其他各界力量，努力建设成具有国际影响力的人工智能开源开放平台与社区。")
            time.sleep(3)
            wechat_instance.send_text(to_wxid=from_wxid, content=f"入群后，您可以和启智社区的开发者进行交流。若您在使用中有任何问题，您可以在群内提出，提问格式可参考：\n 1. 问题描述:\n2. 相关环境：GPU / NPU\n3. 相关集群：启智/智算\n4. 任务名：\n5. 问题截图or log：")
            time.sleep(1)
            wechat_instance.add_room_member(room_wxid=room_wxid, member_list=member)
            time.sleep(1)
            wechat_instance.send_room_at_msg(to_wxid=room_wxid, content="{$@},欢迎加入启智社区！", at_list=member)

        elif data["msg"].split(' ')[0] == '文心' :
            wechat_instance.send_text(to_wxid=from_wxid, content=f"好哦~请您稍等~！")
        
            module = hub.Module(name="ernie_vilg")

            style_input = data['msg'].split(' ')[1]
            text_prompts = data["msg"].split(' ')[2]

            if style_input and not '油画' and not "水彩" and not "粉笔画" and not "卡通" and not "儿童画" and not "蜡笔画" and not "探索无限": 
                wechat_instance.send_text(to_wxid=from_wxid, content=f"目前ERNIE-VILG仅支持“油画、水彩、粉笔画、卡通、儿童画、蜡笔画、探索无限”七种风格，您输入的风格不在此列，请检查后重新输入！")
            else:   
                images = module.generate_image(text_prompts=text_prompts, style=style_input,  output_dir='E:\\Open_source\\OpenI\\ernie_vilg_out\\')  
                if images == '存在敏感词, 请重新输入':
                    wechat_instance.send_text(to_wxid=from_wxid, content=f"存在敏感词, 请重新输入")
                else :
                    for i in range(5):
                        time.sleep(3)
                        image_path = 'E:\\Open_source\\OpenI\\ernie_vilg_out\\'+ data['msg'].split(' ')[2] + '_{}.png'.format(i)
                        wechat_instance.send_image(to_wxid=from_wxid, file_path=image_path)
                    time.sleep(5)
                    wechat_instance.send_text(to_wxid=from_wxid, content=f"图像已生成完毕，希望您能喜欢~")


        elif data["msg"].split(' ')[0] == '使用说明' :
            wechat_instance.send_text(to_wxid=from_wxid, content=f'您好~我是OpenI小助手。\n\n1. 回复【加群】可以加入OpenI官方社区。\n\n2. 回复【盘古+input】可体验鹏城·盘古α大模型生成能力。\n如：“盘古 中国和美国和日本和法国和加拿大和澳大利亚的首都分别是哪里？”\n\n3. 回复【文心+风格+prompt】可体验ERNIE-ViLG的AIGC图文生成能力（目前仅支持“水彩”、“油画”、“粉笔画”、“卡通”、“蜡笔画”、“儿童画”、“探索无限”七种风格）。\n如“文心 油画 睡莲”。\n\n其他隐藏功能可自行探索。')


        elif data["msg"].split(' ')[0] == '盘古' :

            model = "pangu-alpha-evolution-2B6-pt"

            prompt_input = data["msg"].split(' ')[1]
            
            result = Infer.generate(model, prompt_input, api_key=pangu_api_key)  # api_key获取请见上文

            wechat_instance.send_text(to_wxid=from_wxid, content=result['results']['generate_text'])



    # 群聊
    elif from_wxid != self_wxid and room_wxid and myself_wxid in data['at_user_list']:

        member = []

        member.append(data['from_wxid'])

        if data['msg'].split('\u2005')[1].split(' ')[0] == '小说续写':

            # 加载模型
            model = hub.Module(name='ernie_zeus')

            text_prompt = data['msg'].split('\u2005')[1].split(' ')[1]

            # 小说续写
            result = model.novel_continuation(
                text=text_prompt
            )
            wechat_instance.send_room_at_msg(to_wxid=room_wxid, content="{$@} "+result, at_list=member)

        
        elif data['msg'].split('\u2005')[1].split(' ')[0] == '完形填空':

            model = hub.Module(name='ernie_zeus')

            # 完形填空

            text_prompt = data['msg'].split('\u2005')[1].split(' ')[1]
            result = model.text_cloze(
                text=text_prompt
            )
            wechat_instance.send_room_at_msg(to_wxid=room_wxid, content="{$@} "+result, at_list=member)


        elif  data['msg'].split('\u2005')[1].split(' ')[0] == '文本摘要':

            model = hub.Module(name='ernie_zeus')

            # 文本摘要

            text_prompt = data['msg'].split('\u2005')[1].split(' ')[1]
            print(text_prompt)
            result = model.text_summarization(
                text=text_prompt
            )
            wechat_instance.send_room_at_msg(to_wxid=room_wxid, content="{$@} "+result, at_list=member)

        elif data['msg'].split('\u2005')[1].split(' ')[0] == '对联续写':

            model = hub.Module(name='ernie_zeus')

            # 对联续写

            text_prompt = data['msg'].split('\u2005')[1].split(' ')[1]
            result = model.couplet_continuation(
                text=text_prompt
            )
            wechat_instance.send_room_at_msg(to_wxid=room_wxid, content="{$@} "+result, at_list=member)

        elif data['msg'].split('\u2005')[1].split(' ')[0] == '文案创作':

            model = hub.Module(name='ernie_zeus')

            # 文案创作

            text_prompt = data['msg'].split('\u2005')[1].split(' ')[1]
            result = model.copywriting_generation(
                text=text_prompt
            )
            wechat_instance.send_room_at_msg(to_wxid=room_wxid, content="{$@} "+result, at_list=member)

        elif data['msg'].split('\u2005')[1].split(' ')[0] == '作文创作':


            model = hub.Module(name='ernie_zeus')

            # 作文创作

            text_prompt = data['msg'].split('\u2005')[1].split(' ')[1]
            result = model.composition_generation(
                text=text_prompt
            )
            wechat_instance.send_room_at_msg(to_wxid=room_wxid, content="{$@} "+result, at_list=member)


        elif data['msg'].split('\u2005')[1].split(' ')[0] == 'SQL':

            model = hub.Module(name='ernie_zeus')

            # 文本描述转 SQL 语句

            text_prompt = data['msg'].split('\u2005')[1].split(' ')[1]
            result = model.custom_generation(
                text=text_prompt
            )
            wechat_instance.send_room_at_msg(to_wxid=room_wxid, content="{$@} "+result, at_list=member)

        elif data['msg'].split('\u2005')[1].split(' ')[0] == '情感分析':

            model = hub.Module(name='ernie_zeus')

            # 文本情感分析

            text_prompt = data['msg'].split('\u2005')[1].split(' ')[1]
            result = model.custom_generation(
                text=text_prompt,
                task_prompt='SentimentClassification'
            )

            wechat_instance.send_room_at_msg(to_wxid=room_wxid, content="{$@} "+result, at_list=member)

        elif data['msg'].split('\u2005')[1].split(' ')[0] == '文心' :

            wechat_instance.send_room_at_msg(to_wxid=room_wxid, content="{$@} 好哦~请您稍等~！", at_list=member)


            if data['msg'].split('\u2005')[1].split(' ')[1] and not '油画' and not "水彩" and not "粉笔画" and not "卡通" and not "儿童画" and not "蜡笔画" and not "探索无限": 

                wechat_instance.send_room_at_msg(to_wxid=room_wxid, content="{$@} 目前ERNIE-VILG仅支持“油画、水彩、粉笔画、卡通、儿童画、蜡笔画、探索无限”七种风格，您输入的风格不在此列，请检查后重新输入！", at_list=member)
            else:

                module = hub.Module(name="ernie_vilg")

                style_input = data['msg'].split(' ')[1]
                text_prompts = data["msg"].split(' ')[2]

                images = module.generate_image(text_prompts=text_prompts, style=style_input,  output_dir='E:\\Open_source\\OpenI\\ernie_vilg_out\\')  
                print(images)

                if images == '存在敏感词, 请重新输入':
                    wechat_instance.send_room_at_msg(to_wxid=room_wxid, content="{$@} 存在敏感词, 请重新输入", at_list=member)
                    
                else :
                    for i in range(5):
                        time.sleep(3)
                        image_path = 'E:\\Open_source\\OpenI\\ernie_vilg_out\\'+ data['msg'].split(' ')[2] + '_{}.png'.format(i)
                        wechat_instance.send_image(to_wxid=room_wxid, file_path=image_path)
                    time.sleep(5)
                    wechat_instance.send_room_at_msg(to_wxid=room_wxid, content="{$@} 图像已生成完毕，希望您能喜欢~", at_list=member)


        elif data['msg'].split('\u2005')[1].split(' ')[0] == 'pai':
            wechat_instance.send_room_at_msg(to_wxid=room_wxid, content="{$@} 请您稍等，图像正在生成中，大约需要30s~", at_list=member)

            # 默认模型为 pai-painter-painting-base-zh
            text_to_image = Taskflow("text_to_image")

            text_prompt = data['msg'].split('\u2005')[1].split(' ')[1]
            image_list = text_to_image(text_prompt)

            for i in range(2):
                time.sleep(3)
                image_path = 'E:\\Open_source\\OpenI\\ernie_vilg_out\\'+ data['msg'].split(' ')[1] + '_{}.png'.format(i)
                image_list[0][1].save(image_path)
                wechat_instance.send_image(to_wxid=room_wxid, file_path=image_path)

            time.sleep(5)
            wechat_instance.send_room_at_msg(to_wxid=room_wxid, content="{$@} 图像已生成完毕，希望您能喜欢~", at_list=member)

        else :

            model = "pangu-alpha-evolution-2B6-pt"
            text = data['msg'].split('\u2005')[1]
            result = Infer.generate(model, text, api_key=pangu_api_key)  # api_key获取请见上文
            wechat_instance.send_room_at_msg(to_wxid=room_wxid, content="{$@} "+ result['results']['generate_text'], at_list=member)



# 以下是为了让程序不结束，如果有用于PyQt等有主循环消息的框架，可以去除下面代码
try:
    while True:
        time.sleep(0.5)
except KeyboardInterrupt:
    ntchat.exit_()
    sys.exit()
