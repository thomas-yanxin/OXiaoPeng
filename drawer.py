# 以下部分代码摘录自：https://github.com/CrazyBoyM/nonebot-plugin-drawer/blob/main/nonebot_plugin_drawer/drawer.py

import asyncio
import numbers
import os
import urllib.request

import httpx
from pydantic import BaseSettings


class Config(BaseSettings):
    wenxin_ak: str = "G26BfAOLpGIRBN5XrOV2eyPA25CE01lE"  # 文心大模型的ak
    wenxin_sk: str = "txLZOWIjEqXYMU3lSm05ViW4p9DWGOWs"  # 文心大模型的sk
    wenxin_cd_time: int = 60  # cd时间，单位秒
    wenxin_image_count: int = 3  # 画画的图片数量
    wenxin_manager_list: list = []  # 文心大模型的管理员列表（不受冷却时间限制）
    class Config:
        extra = "ignore"

wenxin_config = Config()


# 获取access_token
async def get_token():
  url = "https://wenxin.baidu.com/younger/portal/api/oauth/token"
  async with httpx.AsyncClient(verify=False, timeout=None) as client:
    resp = await client.post(
      url,
      data={
        'grant_type': 'client_credentials',
        'client_id': wenxin_config.wenxin_ak,
        'client_secret': wenxin_config.wenxin_sk
      },
      headers={
        'Content-Type': 'application/x-www-form-urlencoded'
      }
    )
    access_token = resp.json()['data']
    print(access_token)

    return access_token

# 获取绘画的任务id
async def get_taskId(access_token, text, style):

  url = "https://wenxin.baidu.com/younger/portal/api/rest/1.0/ernievilg/v1/txt2img?from=baicai"
  payload = {
    'access_token': access_token,
    'text': text,
    'style': style,
  } # 请求参数
  async with httpx.AsyncClient(verify=False, timeout=None) as client:
    resp = await client.post(url, data=payload)
    data = resp.json()
    print(data)
    if data['code'] == 0: # 请求成功
      return data['data']['taskId']
    
    print(f'绘画任务失败,返回msg: {data["msg"]}') # 请求失败的消息提示
    return None
    

# 获取绘画的结果
async def get_img(access_token, taskId):
  url = "https://wenxin.baidu.com/younger/portal/api/rest/1.0/ernievilg/v1/getImg?from=baicai"
  payload={
    'access_token': access_token,
    'taskId': taskId
  } # 请求参数，taskId是绘画的任务id
  async with httpx.AsyncClient(verify=False, timeout=None) as client:
    resp = await client.post(url, data=payload)
    data = resp.json()
    print(data)
    if data['code'] == 0: # 请求成功
      print(data)
      if data['data']['status'] == 1: # status为1，表明绘画完成
        return data['data']['imgUrls']
      else:
        # 10s后再次请求
        await asyncio.sleep(10)
        return await get_img(access_token, taskId)
    
    print(f'绘画任务失败,返回msg: {data["msg"]}') # 请求失败的消息提示    
    return None


def download(text_prompt, style, number, img_url, file_path):
    #是否有这个路径
    if not os.path.exists(file_path):
    #创建路径
        os.makedirs(file_path)
        #获得图片后缀

    filename = text_prompt + '_' + style + '_'+ number +'.png'
    
    image_path = os.path.join(file_path, filename)
       #下载图片，并保存到文件夹中
    urllib.request.urlretrieve(img_url,filename=image_path)
    return image_path


async def image_url(text, style, file_path):

   access_token = await get_token()

   taskId = await get_taskId(access_token, text, style)
   img = await get_img(access_token, taskId)
   number = 0
   image_path_list = []
   for url in img:
    number += 1
    image_path = download(text, style, str(number), url['image'], file_path)
    image_path_list.append(image_path)
   return image_path_list




