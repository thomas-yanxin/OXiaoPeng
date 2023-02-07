import sys
import time

import ntchat
from revChatGPT.Official import Chatbot

wechat = ntchat.WeChat()
# 打开pc微信, smart: 是否管理已经登录的微信
wechat.open(smart=True)

# 等待登录
wechat.wait_login()

rooms = wechat.get_rooms()

myself_wxid = wechat.get_self_info()['wxid']

openai_key = '******************'

chatbot = Chatbot(api_key=openai_key)

# 注册消息回调
@wechat.msg_register(ntchat.MT_RECV_TEXT_MSG)
def on_recv_text_msg(wechat_instance: ntchat.WeChat, message):
    data = message["data"]
    
    from_wxid = data["from_wxid"]

    self_wxid = wechat_instance.get_login_info()["wxid"]

    room_wxid = data["room_wxid"]
    if from_wxid != self_wxid and not room_wxid:
        
        keyword_input = data["msg"]

        wechat_str = chatbot.ask(keyword_input)
        wechat_instance.send_text(
            to_wxid=from_wxid,
            content=wechat_str
        )
        # 群聊
    elif from_wxid != self_wxid and room_wxid and myself_wxid in data[
            'at_user_list']:

        member = []
        member.append(data['from_wxid'])

        keyword_input = data['msg']

        wechat_str = chatbot.ask(keyword_input)

        wechat_instance.send_room_at_msg(
            to_wxid=room_wxid,
            content="{$@} " + '\n' + wechat_str,
            at_list=member)


# 以下是为了让程序不结束，如果有用于PyQt等有主循环消息的框架，可以去除下面代码
try:
    while True:
        time.sleep(0.5)
except KeyboardInterrupt:
    ntchat.exit_()
    sys.exit()