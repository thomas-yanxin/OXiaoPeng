## 【**欧小鹏**】微信运营机器人

### 产品期待

辅助微信社群运营。受微信群广告机器人困扰太久了...被逼急了自己写个机器人规避一下。


### 更新日志：
- 配置文件模块化，完善repo相关内容；

- 支持基于主人的群转发；

- pangu SaaS服务官方暂时关闭，改用源 1.0；

- 文生图改为异步调用，更符合实际使用环境；

- 文生图能力改为在线调用方式，更加稳定；

- 修复加好友后自动回复的bug；

- 生成图后添加拍一拍；

- 修复敏感词提示的bug；


### 已经支持

1. - [x] 自动添加好友；

2. - [x] 自动拉入对应群聊；

3. - [x] 拉入群聊后@指定对象欢迎；

4. - [x] 接入[Pangu](https://git.openi.org.cn/PCL-Platform.Intelligence/pcl_pangu)SaaS完成日常对话；

5. - [x] 接入[ERNIE-VILG](https://wenxin.baidu.com/moduleApi/ernieVilg) 完成图文生成，接入[ERNIE]完成文章续写等；

6. - [ ] 接入PaddleNlp/RocketQA/Jina完成平台常规使用问题的自动问答；

7. - [x] 群转发

8. - [ ] 待续…

### 部署方式
1. 安装指定[微信PC端](https://git.openi.org.cn/attachments/3bf60134-9d9d-437a-acf4-bfcc50521997?type=0);
2. 安装相关依赖包: `pip install -r requirements.txt`;
3. 补充`config.py`内的相关内容，其中：
    - [wenxin]相关内容可通过[wenxin_key链接](https://wenxin.baidu.com/moduleApi/key)申请获得；
    - [yuan]相关内容可通过[浪潮 源1.0API申请链接](https://air.inspur.com/apply-api)申请获得；
    - [master_wxid]为宿主(master)的初始微信号；
    - [room_wxid]为主营的微信群号，可观察控制台内容获取；
3. 运行main.py文件.


### 特别感谢

1. [ntchat](https://github.com/smallevilbeast/ntchat)提供微信机器人框架；
2. [pcl_pangu](https://git.openi.org.cn/PCL-Platform.Intelligence/pcl_pangu)提供SaaS服务；
3. [ERNIE](https://wenxin.baidu.com/)提供相关图文生成接口等服务；
4. [Yuan-1.0](https://air.inspur.com/home)提供相关问答服务；

### 扫码体验
目前本项目仍在开发初期，欢迎大家扫码体验，加群沟通。

【**注意**】：
- 请勿将私密信息发送至**欧小鹏**。
- 请**合法合规、符合微信平台**使用，本代码及作者不对任何事件后果负责。相关AI生成后的结果均为模型生成，概不代表作者观点和看法。  

![](./wechat.jpg)
