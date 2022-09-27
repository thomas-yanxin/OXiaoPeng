### 使用RocketQA完成自动问答

#### 安装

------

```cmd
pip install faiss-cpu
pip install rocketqa
pip install tornado
python -m pip install paddlepaddle==2.2.2 -i https://mirror.baidu.com/pypi/simple
```



#### 创建索引文件

------

- 执行 index.py 文件，生成 index_data 文件

```cmd
$ python.exe index.py zh qadata.txt qadata
```



#### 启动搜索引擎

------

- 执行 rocketqa_service.py 文件，启动 RocketQA 的搜索引擎

```cmd
$ python.exe rocketqa_service.py zh qadata.txt qadata
```



#### 在微信上实现自动问答

------

- 执行 wechat.py 文件，打开 pc 微信，进行自动问答

```cmd
$ python.exe wechat.py
```



##### 通过微信确认自动问答结果

------

请参考图片【wechat.png】。