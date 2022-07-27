import discord
import json
import time
import random
import datetime
from discord.ext import commands

with open('setting.json','r',encoding='utf8') as jfile:
	jdata = json.load(jfile)

async def randomDate(message):
	o_time = message.channel.created_at
	o_message = await message.channel.history(limit=1, after=o_time, oldest_first=True).flatten()
	stTime = o_message[0].created_at
	start = int(stTime.timestamp())
	end = int(time.time())
	t = random.randint(start, end)
	return datetime.datetime.fromtimestamp(t)	

async def search_message(message, attachBool=True, htmlBool=True):
	msg_list = []
	async for i in message.channel.history(limit=100, after= await randomDate(message)):
		if(not(i.author.bot)):
			if(i.content!="" or len(i.attachments)>0):
				if(not(len(i.attachments)>0 and not(attachBool))):
					if(not(i.content.startswith('http') and not(htmlBool))):
						msg_list.append(i)
						if(len(msg_list)>20): break
	return msg_list[random.randint(0, len(msg_list)-1)]



