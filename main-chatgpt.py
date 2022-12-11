import random
import sys
import time

import ntchat
from revChatGPT.revChatGPT import Chatbot

from chatgpt.config import getToken

config = getToken()

user_session = dict()
# 初始化bot
chatbot = Chatbot(config)
wechat = ntchat.WeChat()
# 打开pc微信, smart: 是否管理已经登录的微信
wechat.open(smart=True)


# 等待登录
wechat.wait_login()

rooms = wechat.get_rooms()

myself_wxid = wechat.get_self_info()['wxid']


def get_chat_response(session_id, prompt):
    # 刷新seesion_token
    chatbot.refresh_session()

    if session_id in user_session:
        # 如果在三分钟内再次发起对话则使用相同的会话ID
        if time.time() < user_session[session_id]['timestamp'] + 60 * 3:
            chatbot.conversation_id = user_session[session_id]['conversation_id']
            chatbot.parent_id = user_session[session_id]['parent_id']
        else:
            chatbot.reset_chat()
    else:
        chatbot.reset_chat()
    try:
        resp = chatbot.get_chat_response(prompt, output="text")
        user_cache = dict()
        user_cache['timestamp'] = time.time()
        user_cache['conversation_id'] = resp['conversation_id']
        user_cache['parent_id'] = resp['parent_id']
        user_session[session_id] = user_cache
        return resp['message']
    except Exception as e:
        print(e)
        return f"发生错误: {str(e)}"




# 注册消息回调
@wechat.msg_register(ntchat.MT_RECV_TEXT_MSG)
def on_recv_text_msg(wechat_instance: ntchat.WeChat, message):
    data = message["data"]
    
    from_wxid = data["from_wxid"]

    self_wxid = wechat_instance.get_login_info()["wxid"]

    room_wxid = data["room_wxid"]
    if from_wxid != self_wxid and not room_wxid:
        
        keyword_input = data["msg"]
        random_session_id = str(random.randint(100, 99999))
        wechat_str  = get_chat_response(random_session_id, keyword_input)
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

        random_session_id = str(random.randint(100, 99999))

        wechat_str  = get_chat_response(random_session_id, keyword_input)

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