import discord
import json
import time
import random
import datetime
import os
from discord.ext import commands
from core.search_channel import randomChannel

async def randomDate(channel):
	o_time = channel.created_at
	o_message = [message async for message in channel.history(limit=1, after=o_time, oldest_first=True)]

	stTime = o_message[0].created_at
	start = int(stTime.timestamp())

	#Royal Repair Hotline (RRH)/normal SP random
	if(channel.id == 704152750979678280):
		start = random.choices([1611820000, 1624970000], weights=(1,99))
		start = int(start[0])

	finalMessage = [message async for message in channel.history(limit=1)]
	end = int(finalMessage[0].created_at.timestamp())

	t = random.randint(start, end)
	return datetime.datetime.fromtimestamp(t)	

async def search_message(message, botID, attachBool=True, htmlBool=True):
	msg_list = []
	chosenChannel = await randomChannel(message)
	async for i in chosenChannel.history(limit=15, after= await randomDate(chosenChannel)):
		if(not(i.author.bot)):
			if((i.content!="" or len(i.attachments)>0) and botID not in i.raw_mentions):
				if(not(len(i.attachments)>0 and not(attachBool))):
					if(not(i.content.startswith('http') and not(htmlBool))):
						msg_list.append(i)
						if(len(msg_list)>5): break
	try:
		return msg_list[random.randint(0, len(msg_list)-1)]
	except:
		await message.channel.send(chosenChannel.name+" - Random failed")
		return "Random failed"
	
async def remove_mentions(message):
	mentions = message.mentions
	final_str = message.content

	for mention in mentions:
		final_str = final_str.replace(mention.mention, mention.name)
	
	return final_str
