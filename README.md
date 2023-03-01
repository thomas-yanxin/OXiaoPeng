## 【**欧小鹏**】运营机器人

### 产品期待

辅助社群运营. 受群广告机器人困扰太久了... 被逼急了自己写个机器人规避一下.

扫码加好友, 回复【加群】可体验鹏城·盘古Dialog模型.

### 已经支持

1. - [x] 自动添加好友；
2. - [x] 自动拉入对应群聊；
3. - [x] 拉入群聊后@指定对象欢迎；
4. - [x] 接入[鹏程·盘古Pangu](https://git.openi.org.cn/PCL-Platform.Intelligence/pcl_pangu)、[浪潮源Yuan1.0]()、[元语智能ChatYuan]()等多个语言模型的MaaS; 
5. - [x] 接入[ERNIE-VILG](https://wenxin.baidu.com/moduleApi/ernieVilg) 完成图文生成; 
6. - [x] 接入RocketQA完成平台常规使用问题的自动问答；
7. - [x] 群转发；

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

### 特别感谢

1. [pcl_pangu](https://git.openi.org.cn/PCL-Platform.Intelligence/pcl_pangu)提供MaaS服务; 
2. [ERNIE](https://wenxin.baidu.com/)提供相关图文生成接口等服务; 
3. [Yuan-1.0](https://air.inspur.com/home)提供相关问答服务; 
4. [ChatYuan]()提供类ChatGPT的问答服务

### 扫码体验

![](./wechat.jpg)

【**注意**】:
* 请勿将私密信息发送至**欧小鹏**.
* 请**合法合规、符合微信平台**使用, 本代码及作者不对任何事件后果负责. 相关AI生成后的结果均为模型生成, 概不代表作者观点和看法.  
