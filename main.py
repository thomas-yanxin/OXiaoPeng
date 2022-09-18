# -*- coding: utf-8 -*-
import asyncio
import os
import random
import sys
import time
import xml.dom.minidom

import ntchat
import paddlehub as hub
from paddlenlp import Taskflow
from pcl_pangu.online import Infer
from simhash import Simhash
from wenxin_api.tasks.text_to_image import TextToImage

from drawer import image_url

wechat = ntchat.WeChat()
import config

# 打开pc微信, smart: 是否管理已经登录的微信
wechat.open(smart=True)

# 等待登录
wechat.wait_login()

rooms = wechat.get_rooms()

myself_wxid = wechat.get_self_info()['wxid']
import heapq
import sys

sys.path.append(os.path.abspath(os.curdir))

from yuan_api.inspurai import Example, Yuan, set_yuan_account

file_path = config.config['file_path']

yuan_account = config.config['yuan_account']
yuan_cell_phone_number = config.config['yuan_cell_phone_number']
master_wxid = config.config['master_wxid']
room_wxid = config.config['room_wxid']

set_yuan_account(yuan_account, yuan_cell_phone_number)  # 输入您申请的账号和手机号

# 注册消息回调
@wechat.msg_register(ntchat.MT_RECV_FRIEND_MSG)
def on_recv_text_msg(wechat_instance: ntchat.WeChat, message):
    xml_content = message["data"]["raw_msg"]
    dom = xml.dom.minidom.parseString(xml_content)

    # 从xml取相关参数
    encryptusername = dom.documentElement.getAttribute("encryptusername")
    ticket = dom.documentElement.getAttribute("ticket")
    scene = dom.documentElement.getAttribute("scene")

    # 自动同意好友申请
    wechat_instance.accept_friend_request(encryptusername, ticket, int(scene))


# 注册消息回调
@wechat.msg_register(ntchat.MT_CONTACT_ADD_NOITFY_MSG)
def on_recv_text_msg(wechat_instance: ntchat.WeChat, message):
    data = message["data"]

    wechat_instance.send_text(to_wxid=data["wxid"], content=f"您好~我是欧小鹏，一位能画能文的复合型人工智障。\n\n您可以回复【加群】加入内测交流群暨OpenI启智社区推广群。\n\n回复【盘古+input】可体验鹏城·盘古α大模型生成能力。如：“盘古 中国和美国和日本和法国和加拿大和澳大利亚的首都分别是哪里？”\n\n回复【文心+风格+prompt】可体验ERNIE-ViLG的AIGC图文生成能力（目前支持“水彩”、“油画”、“粉笔画”、“卡通”、“蜡笔画”、“儿童画”、“探索无限”七种风格），如“文心 油画 睡莲”。当然，您也可以和我自由对话。更多能力请加群后体验。")


# 注册消息回调
@wechat.msg_register(ntchat.MT_RECV_TEXT_MSG)
def on_recv_text_msg(wechat_instance: ntchat.WeChat, message):
    data = message["data"]

    from_wxid = data["from_wxid"]

    self_wxid = wechat_instance.get_login_info()["wxid"]

    room_wxid = data["room_wxid"]


    # 判断消息不是自己发的并且不是群消息时，回复对方
    # 私信

    if from_wxid != self_wxid == master_wxid and data["msg"].split(' ')[0] == '转发':
        rooms = wechat.get_rooms()
        for i, room in enumerate(rooms):
            print(room,self_wxid, room['manager_wxid'])
            if room['is_manager'] == '1':
                room_wxid = room['wxid']
                result = data["msg"].split(' ')[1]
                wechat_instance.send_room_at_msg(to_wxid=room_wxid, content="{$@},"+result,at_list=['notify@all'])

    elif from_wxid != self_wxid and not room_wxid :

        if data["msg"] == '加群':

            member = []
            member.append(data['from_wxid'])


            # else:
            wechat_instance.send_text(to_wxid=from_wxid, content=f"启智社区（简称OpenI）是在国家实施新一代人工智能发展战略背景下，新一代人工智能产业技术创新战略联盟（AITISA）组织产学研用协作共建共享的开源平台与社区，以鹏城云脑科学装置及Trustie软件开发群体化方法为基础，全面推动人工智能领域的开源开放与协同创新。社区在“开源开放、尊重创新”的原则下，汇聚学术界、产业界及社会其他各界力量，努力建设成具有国际影响力的人工智能开源开放平台与社区。")
            sleep_time = random.randint(0,4)
            time.sleep(sleep_time)
            wechat_instance.send_text(to_wxid=from_wxid, content=f"入群后，您可以和启智社区的开发者进行交流。若您在使用中有任何问题，您可以在群内提出，提问格式可参考：\n 1. 问题描述:\n2. 相关环境：GPU / NPU\n3. 相关集群：启智/智算\n4. 任务名：\n5. 问题截图or log：")
            sleep_time = random.randint(0,4)
            time.sleep(sleep_time)
            wechat_instance.add_room_member(room_wxid=room_wxid, member_list=member)
            sleep_time = random.randint(0,4)
            time.sleep(sleep_time)
            wechat_instance.send_room_at_msg(to_wxid=room_wxid, content="{$@},欢迎加入欧小鹏内测交流群！详细内容可看群公告~\nGithub地址：https://github.com/thomas-yanxin/Wechat_bot;\nOpenI启智地址：https://git.openi.org.cn/Learning-Develop-Union/Wechat_bot\nPrompt可参考：https://github.com/PaddlePaddle/PaddleHub/blob/develop/modules/image/text_to_image/ernie_vilg/README.md#%E5%9B%9B-prompt-%E6%8C%87%E5%8D%97\n谢谢关注哇~", at_list=member)


        elif data["msg"].split(' ')[0] == '文心' :
            
            style_input = data['msg'].split(' ')[1]
            text_prompt = data["msg"].split(' ')[2]
            n = 0
            if style_input not in ['油画', "水彩", "粉笔画", "卡通", "儿童画", "蜡笔画", "探索无限"]: 
                wechat_instance.send_text(to_wxid=from_wxid, content=f"目前ERNIE-VILG仅支持“油画、水彩、粉笔画、卡通、儿童画、蜡笔画、探索无限”七种风格，您输入的风格不在此列，请检查后重新输入！")
            else:   
                wechat_instance.send_text(to_wxid=from_wxid, content=f"好哦~ 正在作画，请您耐心等待~！")
                # data_image = ernie_vilg(text_prompt, style_input)  
                # if type(data_image) == 'str':
                #     wechat_instance.send_text(to_wxid=from_wxid, content=f"对不起，您的输入存在敏感词, 请重新输入")
                image_list = asyncio.run(image_url(text=text_prompt, style=style_input, file_path=file_path))
                for image_path in image_list:
                    time.sleep(1)
                    wechat_instance.send_image(to_wxid=from_wxid, file_path=image_path)

                time.sleep(5)
                wechat_instance.send_text(to_wxid=from_wxid, content=f"图像已生成完毕，希望您能喜欢~")


        elif data["msg"].split(' ')[0] == '使用说明' :
            wechat_instance.send_text(to_wxid=from_wxid, content=f'您好~我是欧小鹏，一位能画能文的复合型人工智障。\n\n您可以回复【加群】加入内测交流群。\n\n回复【盘古+input】可体验鹏城·盘古α大模型生成能力。如：“盘古 中国和美国和日本和法国和加拿大和澳大利亚的首都分别是哪里？”\n\n回复【文心+风格+prompt】可体验ERNIE-ViLG的AIGC图文生成能力（目前支持“水彩”、“油画”、“粉笔画”、“卡通”、“蜡笔画”、“儿童画”、“探索无限”七种风格），如“文心 油画 睡莲”。更多能力请加群后体验。若私聊界面无响应，请加群后@群主反馈。')


        elif data["msg"].split(' ')[0] == '盘古' :
                        # 自由问答
            yuan = Yuan(engine="dialog",
            input_prefix="对话：“",
            input_suffix="”",
            output_prefix="答：“",
            output_suffix="”",
            append_output_prefix_to_query=False)

            # model = hub.Module(name='ernie_zeus')
            text_prompt = data["msg"].split(' ')[1]
            try:
                response = yuan.submit_API(prompt=text_prompt,trun="”")
                response = response.split('“')[1]
                wechat_instance.send_text(to_wxid=from_wxid, content=response)

            except:
                wechat_instance.send_text(to_wxid=from_wxid, content='存在敏感词，请重新输入！')

            # model = "pangu-alpha-evolution-2B6-pt"

            # prompt_input = data["msg"].split(' ')[1]
            
            # result = Infer.generate(model, prompt_input, api_key=pangu_api_key)  # api_key获取请见上文

            # wechat_instance.send_text(to_wxid=from_wxid, content=result['results']['generate_text'])

        else:
            yuan = Yuan(engine="dialog",
            input_prefix="对话：“",
            input_suffix="”",
            output_prefix="答：“",
            output_suffix="”",
            append_output_prefix_to_query=False)

            # model = hub.Module(name='ernie_zeus')
            text_prompt = data['msg']

            # 自由问答
            try:
                response = yuan.submit_API(prompt=text_prompt,trun="”")
                response = response.split('“')[1]
                
                wechat_instance.send_text(to_wxid=from_wxid, content= response)
            except :
                wechat_instance.send_text(to_wxid=from_wxid, content="存在敏感词，请重新输入！")
                pass


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

            if data['msg'].split('\u2005')[1].split(' ')[1] not in ['油画', "水彩", "粉笔画", "卡通", "儿童画", "蜡笔画", "探索无限"] : 

                wechat_instance.send_room_at_msg(to_wxid=room_wxid, content="{$@} 目前ERNIE-VILG仅支持“油画、水彩、粉笔画、卡通、儿童画、蜡笔画、探索无限”七种风格，您输入的风格不在此列，请检查后重新输入！", at_list=member)
            else:
                wechat_instance.send_room_at_msg(to_wxid=room_wxid, content="{$@} 好哦~请您稍等~！", at_list=member)
                style_input = data['msg'].split(' ')[1]
                text_prompt = data["msg"].split(' ')[2]

                try:
                    image_list = asyncio.run(image_url(text=text_prompt, style=style_input, file_path=file_path))
                    for i, image_path in enumerate(image_list):
                        time.sleep(1)

                        wechat_instance.send_image(to_wxid=room_wxid, file_path=image_path)
                        if i == 2:
                            break

                    time.sleep(6)
                    wechat_instance.send_room_at_msg(to_wxid=room_wxid, content="{$@}"+"作画: "+ '“' + text_prompt + "”"+ "已生成完毕，希望您能喜欢~", at_list=member)
                    time.sleep(1)
                    wechat_instance.send_pat(room_wxid=room_wxid, patted_wxid=data['from_wxid'])
                except:
                    wechat_instance.send_room_at_msg(to_wxid=room_wxid, content="{$@} "+ '存在敏感词，请重新输入', at_list=member)


        # elif data['msg'].split('\u2005')[1].split(' ')[0] == 'pai':
        #     wechat_instance.send_room_at_msg(to_wxid=room_wxid, content="{$@} 请您稍等，图像正在生成中，大约需要30s~", at_list=member)

        #     # 默认模型为 pai-painter-painting-base-zh
        #     text_to_image = Taskflow("text_to_image")

        #     text_prompt = data['msg'].split('\u2005')[1].split(' ')[1]
        #     image_list = text_to_image(text_prompt)

        #     for i in range(2):
        #         image_path = file_path + data['msg'].split(' ')[1] + '_{}.png'.format(i)
        #         image_list[0][1].save(image_path)
        #         wechat_instance.send_image(to_wxid=room_wxid, file_path=image_path)

        #     time.sleep(5)
        #     wechat_instance.send_room_at_msg(to_wxid=room_wxid, content="{$@} 图像已生成完毕，希望您能喜欢~", at_list=member)
        #     time.sleep(1)
        #     wechat_instance.send_pat(room_wxid=room_wxid, patted_wxid=data['from_wxid'])


        # elif data['msg'].split('\u2005')[1].split(' ')[0] == 'pai风景':
        #     wechat_instance.send_room_at_msg(to_wxid=room_wxid, content="{$@} 请您稍等，图像正在生成中，大约需要30s~", at_list=member)

        #     # 默认模型为 pai-painter-painting-base-zh
        #     text_to_image = Taskflow("text_to_image", model='pai-painter-scenery-base-zh')

        #     text_prompt = data['msg'].split('\u2005')[1].split(' ')[1]
        #     image_list = text_to_image(text_prompt)

        #     for i in range(2):
        #         image_path = file_path + data['msg'].split(' ')[1] + '_{}.png'.format(i)
        #         image_list[0][1].save(image_path)
        #         time.sleep(1)
        #         wechat_instance.send_image(to_wxid=room_wxid, file_path=image_path)

        #     time.sleep(5)
        #     wechat_instance.send_room_at_msg(to_wxid=room_wxid, content="{$@} 图像已生成完毕，希望您能喜欢~", at_list=member)
        #     time.sleep(1)
        #     wechat_instance.send_pat(room_wxid=room_wxid, patted_wxid=data['from_wxid'])


        else :
            yuan = Yuan(engine="dialog",
            input_prefix="对话：“",
            input_suffix="”",
            output_prefix="答：“",
            output_suffix="”",
            append_output_prefix_to_query=False)

            # model = hub.Module(name='ernie_zeus')
            text_prompt = data['msg'].split('\u2005')[1]

            # 自由问答
            try:
                response = yuan.submit_API(prompt=text_prompt,trun="”")
                response = response.split('“')[1]
                
                wechat_instance.send_room_at_msg(to_wxid=room_wxid, content="{$@} "+ response, at_list=member)
            except :
                wechat_instance.send_room_at_msg(to_wxid=room_wxid, content="{$@} "+ '存在敏感词，请重新输入', at_list=member)
                pass
            # model = "pangu-alpha-evolution-2B6-pt"
            # text = data['msg'].split('\u2005')[1]
            # result = Infer.generate(model, text, api_key=pangu_api_key)  # api_key获取请见上文

            # wechat_instance.send_room_at_msg(to_wxid=room_wxid, content="{$@} "+ result['results']['generate_text'], at_list=member)


# 以下是为了让程序不结束，如果有用于PyQt等有主循环消息的框架，可以去除下面代码
try:
    while True:
        time.sleep(0.5)
except KeyboardInterrupt:
    ntchat.exit_()
    sys.exit()
