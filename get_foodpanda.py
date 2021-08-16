import requests as rq
import json
import os
import discord as dc
import asyncio
from discord.ext import commands
from dotenv import load_dotenv

bot=commands.Bot(command_prefix='!')

payload={"q":"starbucks","location":{"point":{"latitude":22.6394924,"longitude":120.302583}},"config":"Variant21","customer_id  ":"","vertical_types":["restaurants"],"include_component_types":["vendors"],"include_fields":["feed"],"language_id":"6","opening    _type":"delivery","platform":"web","session_id":"","language_code":"zh","customer_type":"regular","limit":10,"offset":0,"dps_se  ssion_id":"eyJzZXNzaW9uX2lkIjoiMzhhOGUwZTBmYTllZmNlMGIzZTM4ZjNkZDFiMzE4ZjkiLCJwZXJzZXVzX2lkIjoiMTYyODg0ODk0NC42NTQzNzg4MjU2LjQxe    E05NHIxSDgiLCJ0aW1lc3RhbXAiOjE2Mjg5NDYwMDV9","dynamic_pricing":0,"brand":"foodpanda","country_code":"tw","use_free_delivery_la  bel":False}

headers = {
        'content-type': "application/json",
    }

@bot.event
async def on_ready():
    channel=bot.get_channel(871443543732912163)
    await channel.send('點餐機器人啟動')

used=False
entered=False
keyword=''

@bot.event
async def on_message(message):
    string=message.content
    if string.startswith('init') :
        string,a,b=string.split(' ')
        global payload
        global entered
        payload['latitude']=float(a)
        payload['longitude']=float(b)
        entered=True
        await message.channel.send('定位成功 !')

    elif string.startswith('search') :
        global used
        global keyword

        if entered==False :
            await message.channel.send('請先輸入座標')
        elif used==True :
            await message.channel.send('已經開始一個查詢')
        else :
            used=True
            string,a=string.split(' ')
            keyword=a

            now_payload=payload
            now_payload['q']=keyword
            r=rq.post('https://disco.deliveryhero.io/search/api/v1/feed',data=json.dumps(now_payload),headers=headers)
            print(r.text)
            rt_list=json.loads(r.text)
            r_list=rt_list['feed']['items'][0]['items']
        
            embed = dc.Embed(
                title='請選擇所要的餐廳'
            )
            for i in range(1,6) :
                embed.add_field(name=f'{i}. {r_list[i-1]["name"]}',value=f'評價{r_list[i-1]["rating"]}顆星',inline=False)

            await message.channel.send(embed=embed)
        
    elif string.startswith('clear') :
            used=False
            await message.channel.send('查詢資料清除成功')

        













load_dotenv()
bot.run(os.getenv('TOKEN'))
