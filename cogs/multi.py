import discord
import json
from discord.ext import commands
from core.classes import Cog_Extension
from core.search_message import search_message, stDate

with open('setting.json','r',encoding='utf8') as jfile:
	jdata = json.load(jfile)

class multi(Cog_Extension):	
	@commands.command(aliases=['miko'])
	async def m(self, message, num=4):
		if(num > jdata['mLimit']):
			await message.channel.send("Too much")
			return
		if(num < 1):
			await message.channel.send("?")
			return
		await message.channel.send("正如同底下這段對話所表達的:")
		startDate = await stDate(message)
		for i in range(num):
			msg = await search_message(message, startDate, attachBool=False, htmlBool=False)
			if(len(msg.attachments)<=0):
				await message.channel.send('"'+msg.content+'"')
			else:
				i=msg.attachments[0]
				await message.channel.send(i.url)
def setup(bot):
	bot.add_cog(multi(bot))


