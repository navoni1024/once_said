import discord
import json
import time
import random
import datetime
from discord.ext import commands

with open('setting.json','r',encoding='utf8') as jfile:
	jdata = json.load(jfile)

def randomDate(i):
	start = int(i.timestamp())
	end = int(time.time())
	t = random.randint(start, end)
	return datetime.datetime.fromtimestamp(t)

async def stDate(message):
	o_time = message.channel.created_at
	o_message = await message.channel.history(limit=1, after=o_time, oldest_first=True).flatten()
	return o_message[0].created_at

async def search_message(message, date, attachBool=True, htmlBool=True):
	msg_list = []
	botID = jdata['botID']
	async for i in message.channel.history(limit=100, around=randomDate(date)):
		if(not(i.author.bot) and i.content != botID[0] and i.content != botID[1]):
			if(i.content!="" or len(i.attachments)>0):
				if(not(len(i.attachments)>0 and not(attachBool))):
					if(not(i.content.startswith('http') and not(htmlBool))):
						msg_list.append(i)
						if(len(msg_list)>30): break
	return msg_list[random.randint(0, len(msg_list)-1)]



