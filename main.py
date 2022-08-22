from datetime import date, datetime
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random

today = datetime.now()
start_date = os.environ['START_DATE']
city = os.environ['CITY']
birthday = os.environ['BIRTHDAY']

app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]

user_id = os.environ["USER_ID"]
template_id = os.environ["TEMPLATE_ID"]

def get_week():
  week_list = ["星期一","星期二","星期三","星期四","星期五","星期六","星期日"]
  return week_list[datetime.now().weekday()]

def get_weather():
  url = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=" + city
  res = requests.get(url).json()
  weather = res['data']['list'][0]
  return weather['weather'], math.floor(weather['temp'])

def get_tips():
  url = "https://devapi.qweather.com/v7/indices/1d?"
  params = {"location": "120.13,36.55",
            "key": "d999a452f7eb4718b3c237d9778f4a7f",
            "type": "3"
           }
  response = requests.get(url, params).json()
  tips = response['daily']['text']
  return tips
    
def get_count():
  delta = today - datetime.strptime(start_date, "%Y-%m-%d")
  return delta.days

def get_birthday():
  next = datetime.strptime(str(date.today().year) + "-" + birthday, "%Y-%m-%d")
  if next < datetime.now():
    next = next.replace(year=next.year + 1)
  return (next - today).days

def get_words():
  words = requests.get("https://api.shadiao.pro/chp")
  if words.status_code != 200:
    return get_words()
  return words.json()['data'][0]['text']

def get_random_color():
  return "#%06x" % random.randint(0, 0xFFFFFF)


client = WeChatClient(app_id, app_secret)

wm = WeChatMessage(client)
wea, temperature = get_weather()
data = {"time":{"value":"%s"%date.today()+"  "+"%s"%get_week(), "color":get_random_color()},"city":{"value":"青岛", "color":get_random_color()},"weather":{"value":wea, "color":get_random_color()},"temperature":{"value":temperature, "color":get_random_color()},"tips":{"value":get_tips(),"color":get_random_color()},"love_days":{"value":get_count(), "color":get_random_color()},"birthday_left":{"value":"距离小可爱的生日还有"+"%d"%get_birthday()+"天", "color":get_random_color()},"words":{"value":get_words(), "color":get_random_color()}}
res = wm.send_template(user_id, template_id, data)
print(res)
