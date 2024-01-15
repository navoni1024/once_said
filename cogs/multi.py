import discord
import json
from discord.ext import commands
from core.classes import Cog_Extension
from core.search_message import search_message

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

		resultMsg = ""
		
		for i in range(num):
			msg = await search_message(message, botID=self.bot.user.id, attachBool=False, htmlBool=False)
			if(msg=="Random failed"):
				continue
			if(len(msg.attachments)<=0):
				resultMsg+='"'+msg.content+'"\n'
			else:
				i=msg.attachments[0]
				resultMsg+=i.url+'\n'

		await message.channel.send(resultMsg)

def setup(bot):
	bot.add_cog(multi(bot))


