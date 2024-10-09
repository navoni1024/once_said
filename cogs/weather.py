from discord.ext import commands
from core.cwb import cwb

class weather(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.settings = bot.settings
	
	@commands.command(aliases=['weather'])
	async def w(self, message, location='台北市'):
		await message.channel.send("正如同**中央氣象局**曾經說過的")
		await message.channel.send(cwb(location, self.settings['API_KEY']))

async def setup(bot):
	await bot.add_cog(weather(bot))	