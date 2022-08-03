import discord
import json
from discord.ext import commands
from core.classes import Cog_Extension
from core.search_message import search_message

with open('setting.json','r',encoding='utf8') as jfile:
	jdata = json.load(jfile)

class listen(Cog_Extension):	
	@commands.Cog.listener()
	async def on_message(self, message):
		if(message.author.bot): return
		if (self.bot.user.id in message.raw_mentions):
			msg = await search_message(message, botID=self.bot.user.id, htmlBool=False)
		else:
			return
		header = "正如同**"+str(msg.author.name)+"**曾經"
		if(msg.content!=""): header += "說過"
		if(msg.content!="" and len(msg.attachments)>0): header += "和"
		if(len(msg.attachments)>0): header+="傳過"
		header += "的"
		await message.channel.send(header)
		if(msg.content!=""): await message.channel.send('"'+msg.content+'"')
		photoLimit = jdata['photoLimit']
		for attachment in msg.attachments:
			await message.channel.send(attachment.url)
			photoLimit-=1
			if(photoLimit<=0): break

def setup(bot):
	bot.add_cog(listen(bot))


