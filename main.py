# -*- coding: utf-8 -*-
import asyncio
import json
import os
import random
import sys
import time
import xml.dom.minidom

import ntchat
import requests

sys.path.append(os.path.abspath(os.curdir))

from wechatbot import common_const, config
from wechatbot.drawer import image_url

wechat = ntchat.WeChat()
wechat.open(smart=True)
wechat.wait_login()
rooms = wechat.get_rooms()

nickname = wechat.get_self_info()['nickname']
master_wxid = config.config['master_wxid']

indirect_num = 0
for indirect_list in rooms:
    indirect_num += indirect_list['total_member']

myself_wxid = wechat.get_self_info()['wxid']
direct_num = len(wechat.get_contacts())
print('直接用户：%d人' % direct_num, '间接用户：%d人' % indirect_num,
      '群聊数量：%d' % len(rooms))


def yuan_1_0(text_prompt):
    model_name = 'yuan'
    # # 自由问答
    try:
        from yuan_api.inspurai import Example, Yuan, set_yuan_account
        yuan_account = config.config['yuan_account']
        yuan_cell_phone_number = config.config['yuan_cell_phone_number']
        set_yuan_account(yuan_account, yuan_cell_phone_number)
        yuan = Yuan(engine="dialog",
                    topK=5,
                    input_prefix="对话：“",
                    input_suffix="”",
                    output_prefix="答：“",
                    output_suffix="”",
                    append_output_prefix_to_query=False)
        text_prompt = text_prompt
        response = yuan.submit_API(prompt=text_prompt, trun="”")
        response = response.split('“')[1]
    except:
        response = "任务存在问题"
    return response


def ChatYuan(text_prompt):
    model_name = 'ChatYuan'
    try:
        import clueai
        clueai_key = config.config['clueai_key']
        # initialize the Clueai Client with an API Key
        cl = clueai.Client(clueai_key, check_api_key=True)
        prompt = "用户：" + text_prompt + "\n小元："
        # generate a prediction for a prompt
        # 需要返回得分的话，指定return_likelihoods="GENERATION"
        prediction = cl.generate(model_name='ChatYuan-large', prompt=prompt)
        # print the predicted text
        print('prediction: {}'.format(prediction.generations[0].text))
        response = prediction.generations[0].text
    except:
        response = "任务存在问题"
    return response


def ChatPanGu(text_prompt):
    model_name = 'chatpangu'
    model = "chat-pangu"
    prompt_input = []
    try:
        from pcl_pangu.online import Infer
        api_key = config.config['PanGu_key']
        prompt_input.append(text_prompt)
        result = Infer.generate(model, prompt_input, api_key)
        response = result['results']['generate_text']
    except:
        response = "任务存在问题"
    return response


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

    wechat_instance.send_text(
        to_wxid=data["wxid"],
        content=
        f"您好~我是欧小鹏，一位能画能文的复合型人工智障。\n目前欧小鹏支持：\n\n1. 【文生图能力】交互方式：文心 风格 描述，（支持“古风、油画、水彩画、粉笔画、卡通画、二次元、浮世绘、蒸汽波艺术、像素风格、概念艺术、未来主义、赛博朋克、写实风格、洛丽塔风格、巴洛克风格、超现实主义”风格），如：“文心 概念艺术 启智社区”；\n\n2. 【平台问答】交互方式：QA 描述，如：“QA 数据集上传”；\n\n3. 【自动问答】\n(1) ChatYuan模型：元语 描述\n(2) 源1.0模型：源 描述\n(3) ChatGPT: chat 描述\n(4) 鹏程·盘古对话模型：直接描述\n\n【注】：群聊内需@欧小鹏才可触发上述功能，且@是真正@，并非复制！更多能力请回复【加群】后体验。若体验存在问题，请加群后反馈。"
    )


# 注册消息回调
@wechat.msg_register(ntchat.MT_RECV_TEXT_MSG)
def on_recv_text_msg(wechat_instance: ntchat.WeChat, message):

    data = message["data"]
    from_wxid = data["from_wxid"]
    self_wxid = wechat_instance.get_login_info()["wxid"]
    room_wxid = data["room_wxid"]

    # 判断消息不是自己发的并且不是群消息时，回复对方

    if from_wxid != self_wxid and not room_wxid:

        if data["msg"] == '加群':
            try:
                room_wxid = config.config['room_wxid']
                member = []
                member.append(data['from_wxid'])

                sleep_time = random.randint(0, 4)
                time.sleep(sleep_time)
                wechat_instance.invite_room_member(room_wxid=room_wxid,
                                                   member_list=member)
                sleep_time = random.randint(0, 4)
                time.sleep(sleep_time)
            except:
                wechat_instance.send_text(to_wxid=from_wxid,
                                          content=f"任务存在问题，请联系作者")

        elif data["msg"].split(' ')[0] == '菜单':
            wechat_instance.send_text(
                to_wxid=from_wxid,
                content=
                f'您好~我是欧小鹏，一位能画能文的复合型人工智障。\n目前欧小鹏支持：\n\n1. 【文生图能力】交互方式：文心 风格 描述，（支持“古风、油画、水彩画、粉笔画、卡通画、二次元、浮世绘、蒸汽波艺术、像素风格、概念艺术、未来主义、赛博朋克、写实风格、洛丽塔风格、巴洛克风格、超现实主义”风格），如：“文心 概念艺术 启智社区”；\n\n2. 【平台问答】交互方式：QA 描述，如：“QA 数据集上传”；\n\n3. 【ISSUE创建】交互方式：issue 描述，如：“issue 平台此处存在改进空间”；\n\n4. 【自动问答】\n(1) ChatYuan模型：元语 描述\n(2) 源1.0模型：源 描述\n(3) ChatGPT: chat 描述\n(4) 鹏程·盘古对话模型：直接描述\n\n【注】：群聊内需@欧小鹏才可触发上述功能，且@是真正@，并非复制！更多能力请回复【加群】后体验。若体验存在问题，请加群后反馈。'
            )

        elif data["msg"].split(' ')[0] == '文心':

            style_input = data['msg'].split(' ')[1]
            text_prompt = data["msg"].split(' ')[2]
            n = 0
            if style_input not in [
                    '古风', '油画', "水彩画", "卡通画", '二次元', '浮世绘', '蒸汽波艺术', '像素风格',
                    '概念艺术', '未来主义', '赛博朋克', '写实风格', '洛丽塔风格', '巴洛克风格', '超现实主义',
                    "探索无限"
            ]:
                wechat_instance.send_text(
                    to_wxid=from_wxid,
                    content=
                    f"目前ERNIE-VILG仅支持“古风、油画、水彩画、卡通画、二次元、浮世绘、蒸汽波艺术、像素风格、概念艺术、未来主义、赛博朋克、写实风格、洛丽塔风格、巴洛克风格、超现实主义、探索无限”风格，您输入的风格不在此列，请检查后重新输入！"
                )
            else:
                wechat_instance.send_text(to_wxid=from_wxid,
                                          content=f"好哦~ 正在作画，请您耐心等待~！")

                try:
                    file_path = config.config['file_path']
                    image_list = asyncio.run(
                        image_url(text=text_prompt,
                                  style=style_input,
                                  file_path=file_path))
                    for image_path in image_list:
                        time.sleep(1)
                        wechat_instance.send_image(to_wxid=from_wxid,
                                                   file_path=image_path)

                    time.sleep(5)
                    wechat_instance.send_text(to_wxid=from_wxid,
                                              content=f"图像已生成完毕，希望您能喜欢~")
                except:
                    wechat_instance.send_text(to_wxid=from_wxid,
                                              content=f"文生图功能暂时关闭")

        elif from_wxid != self_wxid and not room_wxid and data["msg"].split(
                ' ')[0] == 'QA':
            SERVICE_ADD = 'http://localhost:8888/rocketqa'

            # 判断是否是QA问答关键字，形式为"QA XXXX"，关键字与所咨询的问题之间以一个空格间隔

            keyword_input = data["msg"].split(' ')[1]
            wechat_str = ''

            input_data = {}
            input_data['query'] = keyword_input
            input_data['topk'] = common_const.TOPK

            # 通过RocketQA，按照匹配度由高到低，获取所咨询问题的相关话题
            result = requests.post(SERVICE_ADD, json=input_data)
            res_json = json.loads(result.text)

            if res_json['answer'] is None or len(res_json['answer']) == 0:
                wechat_instance.send_text(to_wxid=from_wxid,
                                          content="未查询到与之匹配的问题，请重新输入咨询内容。")

                return res_json

            i = 0
            for queryIndex in res_json['answer']:

                # 在每套话题之间加上分割线

                if i > 0:
                    wechat_str = wechat_str + "------------------------\r\n"

                wechat_str = wechat_str + "问题" + str(
                    i + 1) + ": " + queryIndex['title'] + '\n'
                wechat_str = wechat_str + "回答" + str(
                    i + 1) + ": " + queryIndex['para'] + '\n'

                i = i + 1

            # 将结果回复对方
            wechat_instance.send_text(to_wxid=from_wxid, content=wechat_str)

        elif data['msg'].split(' ')[0] == '源':
            text_prompt = data['msg'].split(' ')[1]
            response = yuan_1_0(text_prompt=text_prompt)

            wechat_instance.send_text(to_wxid=from_wxid,
                                      content='【浪潮源1.0回复】' + response)

        elif data['msg'].split(' ')[0] == '元语':
            text_prompt = data['msg'].split(' ')[1]
            response = ChatYuan(text_prompt=text_prompt)
            wechat_instance.send_text(to_wxid=from_wxid,
                                      content="【ChatYuan回复】" + response)

        elif data['msg'].split(' ')[0] == '盘古':
            text_prompt = data['msg'].split(' ')[1]
            response = ChatPanGu(text_prompt=text_prompt)
            wechat_instance.send_text(to_wxid=from_wxid,
                                      content="【ChatPanGu回复】" + response)

        else:
            text_prompt = data['msg']
            response = ChatPanGu(text_prompt=text_prompt)

            wechat_instance.send_text(to_wxid=from_wxid,
                                      content="【鹏程·盘古对话模型回复】" + response)

# 群聊
    elif from_wxid != self_wxid and room_wxid and '@' + nickname in data['msg']:
        at_nickname = '@' + nickname
        black_wxid = config.config['black_wxid']
        member = []
        member.append(data['from_wxid'])
        room_wxid = data['room_wxid']
        if '\u2005' in data['msg'].replace(at_nickname, ''):
            base_prompt = data['msg'].replace(at_nickname + '\u2005', '')
        elif at_nickname + ' ' in data['msg']:
            base_prompt = data['msg'].replace(at_nickname + ' ', '')
        else:
            base_prompt = data['msg'].replace(at_nickname, '')

        if data['from_wxid'] not in black_wxid:

            if base_prompt.split(' ')[0] == '文心':

                if base_prompt.split(' ')[1] not in [
                        '古风', '油画', "水彩画", "卡通画", '二次元', '浮世绘', '蒸汽波艺术',
                        '像素风格', '概念艺术', '未来主义', '赛博朋克', '写实风格', '洛丽塔风格',
                        '巴洛克风格', '超现实主义'
                ]:

                    wechat_instance.send_room_at_msg(
                        to_wxid=room_wxid,
                        content=
                        "{$@} 目前ERNIE-VILG仅支持“古风、油画、水彩画、卡通画、二次元、浮世绘、蒸汽波艺术、像素风格、概念艺术、未来主义、赛博朋克、写实风格、洛丽塔风格、巴洛克风格、超现实主义”风格，您输入的风格不在此列，请检查后重新输入！",
                        at_list=member)
                else:
                    wechat_instance.send_room_at_msg(to_wxid=room_wxid,
                                                     content="{$@} 好哦~请您稍等~！",
                                                     at_list=member)
                    style_input = base_prompt.split(' ')[1]
                    text_prompt = base_prompt.split(' ')[2]

                    try:
                        file_path = config.config['file_path']
                        image_list = asyncio.run(
                            image_url(text=text_prompt,
                                      style=style_input,
                                      file_path=file_path))
                        for i, image_path in enumerate(image_list):
                            time.sleep(1)

                            wechat_instance.send_image(to_wxid=room_wxid,
                                                       file_path=image_path)
                            if i == 2:
                                break

                        time.sleep(6)
                        wechat_instance.send_room_at_msg(
                            to_wxid=room_wxid,
                            content="{$@}" + "作画: " + '“' + text_prompt + "”" +
                            "已生成完毕，希望您能喜欢~",
                            at_list=member)
                        time.sleep(1)
                        wechat_instance.send_pat(room_wxid=room_wxid,
                                                 patted_wxid=data['from_wxid'])
                    except:
                        wechat_instance.send_room_at_msg(to_wxid=room_wxid,
                                                         content="{$@} " +
                                                         '文生图功能暂时关闭',
                                                         at_list=member)

            elif base_prompt.split(' ')[0] == 'QA':
                SERVICE_ADD = 'http://localhost:8888/rocketqa'
                # 判断是否是QA问答关键字，形式为"QA XXXX"，关键字与所咨询的问题之间以一个空格间隔

                keyword_input = base_prompt.replace('QA ', '')
                wechat_str = ''
                input_data = {}
                input_data['query'] = keyword_input
                input_data['topk'] = common_const.TOPK

                # 通过RocketQA，按照匹配度由高到低，获取所咨询问题的相关话题
                result = requests.post(SERVICE_ADD, json=input_data)
                res_json = json.loads(result.text)

                if res_json['answer'] is None or len(res_json['answer']) == 0:
                    wechat_instance.send_room_at_msg(to_wxid=room_wxid,
                                                     content="{$@} " +
                                                     "未查询到与之匹配的问题，请咨询群内研发人员。",
                                                     at_list=member)
                    return res_json

                i = 0
                for queryIndex in res_json['answer']:

                    # 在每套话题之间加上分割线
                    if i > 0:
                        wechat_str = wechat_str + "------------------------\r\n"

                    wechat_str = wechat_str + "问题" + str(
                        i + 1) + ": " + queryIndex['title'] + '\n'
                    wechat_str = wechat_str + "回答" + str(
                        i + 1) + ": " + queryIndex['para'] + '\n'
                    i = i + 1
                # 将结果回复对方
                wechat_instance.send_room_at_msg(to_wxid=room_wxid,
                                                 content="{$@} " + '\n' +
                                                 wechat_str,
                                                 at_list=member)

            elif '菜单' in data['msg']:
                wechat_str = '目前欧小鹏支持：\n\n1. 【文生图能力】交互方式：文心 风格 描述，（支持“古风、油画、水彩画、粉笔画、卡通画、二次元、浮世绘、蒸汽波艺术、像素风格、概念艺术、未来主义、赛博朋克、写实风格、洛丽塔风格、巴洛克风格、超现实主义”风格），如：“文心 概念艺术 启智社区”；\n\n2. 【平台问答】交互方式：QA 描述，如：“QA 数据集上传”；\n\n3. 【ISSUE创建】交互方式：issue 描述，如：“issue 平台此处存在改进空间”；\n\n4. 【自动问答】\n(1) ChatYuan模型：元语 描述\n(2) 源1.0模型：源 描述\n(3)  鹏程·盘古对话模型：盘古 描述\n(4) 直接描述则随机模型回复\n\n【注】：\n1. 群聊内需@欧小鹏才可触发上述功能，且@是真正@，并非复制！\n2. 源码：https://github.com/thomas-yanxin/OXiaoPeng\n3. 请勿发送有关私密、ZZ、HS、恶搞等敏感内容至欧小鹏，一经发现，立即拉黑。\n4. 有隐私担忧的用户请勿使用欧小鹏并立即拉黑删除欧小鹏！'
                wechat_instance.send_room_at_msg(to_wxid=room_wxid,
                                                 content="{$@} " + '\n' +
                                                 wechat_str,
                                                 at_list=member)

            elif base_prompt.split(' ')[0] == '源':
                text_prompt = base_prompt.replace('源 ', '')
                response = yuan_1_0(text_prompt=text_prompt)
                wechat_instance.send_room_at_msg(
                    to_wxid=room_wxid,
                    content="{$@} " + "【浪潮源1.0大模型回复】" + '\n' + response,
                    at_list=member)

            elif base_prompt.split(' ')[0] == '元语':

                text_prompt = base_prompt.replace('元语 ', '')
                response = ChatYuan(text_prompt=text_prompt)

                wechat_instance.send_room_at_msg(
                    to_wxid=room_wxid,
                    content="{$@} " + '【ChatYuan模型回复】' + '\n' + response,
                    at_list=member)

            elif base_prompt.split(' ')[0] == '盘古':
                text_prompt = base_prompt.replace('盘古 ', '')
                response = ChatPanGu(text_prompt=text_prompt)

                wechat_instance.send_room_at_msg(
                    to_wxid=room_wxid,
                    content="{$@} " + "【鹏程·盘古对话模型回复】" + '\n' + response,
                    at_list=member)

            else:
                text_prompt = base_prompt
                response = ChatPanGu(text_prompt=text_prompt)
                wechat_instance.send_room_at_msg(
                    to_wxid=room_wxid,
                    content="{$@} " + "【鹏程·盘古对话模型回复】" + '\n' + response,
                    at_list=member)


# 注册监听所有消息回调
@wechat.msg_register(ntchat.MT_ALL)
def on_recv_text_msg(wechat_instance: ntchat.WeChat, message):
    data = message["data"]
    type_wx = message['type']

    if type_wx == 11098:
        data = message['data']
        member_ = data['member_list']
        member_wxid = data['member_list'][0]['wxid']
        member = []
        member.append(member_wxid)
        room_wxid_ = data['room_wxid']
        time.sleep(0.5)
        try:
            main_room_wxid = config.config('room_wxid')
            if room_wxid_ == main_room_wxid:
                sleep_time = random.randint(0, 4)
                time.sleep(sleep_time)
                wechat_instance.send_room_at_msg(
                    to_wxid=room_wxid_,
                    content=
                    "{$@},欢迎加入欧小鹏内测交流群！详细内容可看群公告~\nGithub地址：https://github.com/thomas-yanxin/Wechat_bot\nOpenI启智地址：https://git.openi.org.cn/Learning-Develop-Union/Wechat_bot\nPrompt可参考：https://github.com/PaddlePaddle/PaddleHub/blob/develop/modules/image/text_to_image/ernie_vilg/README.md#%E5%9B%9B-prompt-%E6%8C%87%E5%8D%97\n记得点个star嗷~\n\n（温馨提示：@欧小鹏回复“菜单”可解锁欧小鹏全部能力~）\n\n点击链接即可注册OpenI账号畅想海量免费算力 https://git.openi.org.cn/user/sign_up?sharedUser=thomas-yanxin",
                    at_list=member)
        except:
            pass


# 以下是为了让程序不结束，如果有用于PyQt等有主循环消息的框架，可以去除下面代码
try:
    while True:
        time.sleep(0.5)
except KeyboardInterrupt:
    ntchat.exit_()
    sys.exit()
