from discord.ext import commands
from core.search_message import search_message, remove_mentions

class randomctx(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.settings = bot.settings

	@commands.Cog.listener()
	async def on_message(self, ctx):
		if(ctx.author.bot): return
		if('<@'+str(self.bot.user.id)+'>' == ctx.content):
			msg = await search_message(ctx, botID=self.bot.user.id, htmlBool=False)
			if(msg=="Random failed"):
				return
			else:
				header = "正如同**"+str(msg.author.name)+"**曾經"
				if(msg.content!=""): header += "說過"
				if(msg.content!="" and len(msg.attachments)>0): header += "和"
				if(len(msg.attachments)>0): header+="傳過"
				header += "的"
				await ctx.channel.send(header)
				tmp = await remove_mentions(msg)
				if(msg.content!=""): await ctx.channel.send('"'+tmp+'"')
				photoLimit = self.settings['photoLimit']
				for attachment in msg.attachments:
					await ctx.channel.send(attachment.url)
					photoLimit-=1
					if(photoLimit<=0): break

	@commands.command(aliases=['miko'])
	async def m(self, ctx, num=4):
		if(num > self.settings['mLimit']):
			await ctx.channel.send("Too much")
			return
		if(num < 1):
			await ctx.channel.send("?")
			return
		await ctx.channel.send("正如同底下這段對話所表達的:")

		resultMsg = ""
		
		for i in range(num):
			msg = await search_message(ctx, botID=self.bot.user.id, attachBool=False, htmlBool=False)
			if(msg=="Random failed"):
				continue
			if(len(msg.attachments)<=0):
				tmp = await remove_mentions(msg)
				resultMsg+='"'+tmp+'"\n'
			else:
				i=msg.attachments[0]
				resultMsg+=i.url+'\n'

		await ctx.channel.send(resultMsg)
		

async def setup(bot):
	await bot.add_cog(randomctx(bot))


