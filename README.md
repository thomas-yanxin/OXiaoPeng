## 【**欧小鹏**】运营机器人

### 产品期待

辅助社群运营。受群广告机器人困扰太久了...被逼急了自己写个机器人规避一下。

扫码加好友，回复【加群】可体验ChatGPT（已报废）.

### 已经支持

1. - [x] 自动添加好友；

2. - [x] 自动拉入对应群聊；

3. - [x] 拉入群聊后@指定对象欢迎；

4. - [x] 接入[Pangu](https://git.openi.org.cn/PCL-Platform.Intelligence/pcl_pangu)SaaS完成日常对话（因盘古SaaS服务暂停改用源1.0替代）；

5. - [x] 接入[ERNIE-VILG](https://wenxin.baidu.com/moduleApi/ernieVilg) 完成图文生成；

6. - [x] 接入RocketQA完成平台常规使用问题的自动问答；

7. - [x] 群转发；

8. - [x] chatgpt；



### 部署方式
1. 安装指定[PC端](https://git.openi.org.cn/attachments/3bf60134-9d9d-437a-acf4-bfcc50521997?type=0);
2. 安装相关依赖包: `pip install -r requirements.txt`;
3. 补充`./wechatbot/config.py`内的相关内容，其中：
    - [wenxin]相关内容可通过[wenxin_key链接](https://wenxin.baidu.com/moduleApi/key)申请获得；
    - [yuan]相关内容可通过[浪潮 源1.0API申请链接](https://air.inspur.com/apply-api)申请获得；
    - [master_wxid]为宿主(master)的初始微信号；
    - [room_wxid]为主营的微信群号，可观察控制台内容获取；
4. 创建索引文件: `python3 ./wechatbot/index.py zh ./wechatbot/qadata.txt ./wechatbot/qadata`
5. 启动搜索引擎: `python3 ./wechatbot/rocketqa_service.py zh ./wechatbot/qadata.txt ./wechatbot/qadata`
6. 运行main.py文件.

### chatgpt简易版

1. 安装指定[PC端](https://git.openi.org.cn/attachments/3bf60134-9d9d-437a-acf4-bfcc50521997?type=0);
2.  获取你的 session token(如何注册chatgpt见[此处](https://mirror.xyz/boxchen.eth/9O9CSqyKDj4BKUIil7NC1Sa1LJM-3hsPqaeW_QjfFBc)):
>
> - 打开 [https://chat.openai.com/chat](https://chat.openai.com/chat) 并登录注册，进入网页。
> - 打开浏览器的 dev tools（按 F12）.
> - 从顶栏中选择 Application > Cookies.
>   ![image.png](https://cdn.nlark.com/yuque/0/2022/png/2777249/1670287051371-acd694da-cd3f-46c4-97c4-96438965f8a4.png#averageHue=%232d3136&clientId=uf4023d0a-0da7-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=497&id=u77b3570c&margin=%5Bobject%20Object%5D&name=image.png&originHeight=994&originWidth=1586&originalType=binary&ratio=1&rotation=0&showTitle=false&size=796464&status=done&style=none&taskId=uf4e7e669-4feb-431a-80b7-f7ab47c9113&title=&width=793)
> - `__Secure-next-auth.session-token`就是你的 session token 啦。
3. 替换`./chatgpt/config.py`内的token为自己的token值；
4. `pip install -r requirements-chatgpt.txt`
5. `python main-chatgpt.py`

附：

### 特别感谢

1. [pcl_pangu](https://git.openi.org.cn/PCL-Platform.Intelligence/pcl_pangu)提供SaaS服务；
2. [ERNIE](https://wenxin.baidu.com/)提供相关图文生成接口等服务；
3. [Yuan-1.0](https://air.inspur.com/home)提供相关问答服务；

### 扫码体验
![](https://github.com/thomas-yanxin/OXiaoPeng/blob/master/wechat.jpg)

【**注意**】：
- 请勿将私密信息发送至**欧小鹏**。
- 请**合法合规、符合微信平台**使用，本代码及作者不对任何事件后果负责。相关AI生成后的结果均为模型生成，概不代表作者观点和看法。  
