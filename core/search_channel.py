import discord
import json
import time
import random
import datetime
import tempfile
import os
from discord.ext import commands

async def randomChannel(message):
	channelList = []
	try:
		with open(os.path.join('./filter/',str(message.guild.id)+'.json'),'r',encoding='utf8') as jfile:
			whiteList = json.load(jfile)
			channelList=list(whiteList.values())
		
	except:
		await message.channel.send("Use all channels")
		for i in message.guild.text_channels:
			channelList.append(i.id)
			
	r = random.randint(0, len(channelList)-1)
	return discord.utils.get(message.guild.text_channels, id=channelList[r]) #尋找ID符合隨機出來的ID的頻道傳回去

async def output_channel_list(message):
	channels_list = {_channel.name: _channel.id for _channel in message.guild.channels}
	threads_list = {_threads.name: _threads.id for _threads in message.guild.threads}
	complete_list = {"channels":channels_list, "threads":threads_list}
	complete_list_json = json.dumps(complete_list, indent=4, ensure_ascii=False)
	
	temp_file = tempfile.NamedTemporaryFile(mode='w+', delete=False, encoding='utf-8', suffix='.json')
		
	try:
		temp_file.write(complete_list_json)
		temp_file.close()
		file=discord.File(temp_file.name, filename='complete_list.json')
		await message.channel.send(file=file)

	finally:
		os.unlink(temp_file.name)