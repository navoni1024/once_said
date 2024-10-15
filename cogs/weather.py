from discord.ext import commands
from core.cwb import cwb

class weather(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.settings = bot.settings
		self.url = self.settings["weather_forecast_url"].replace("API_KEY", self.settings["API_KEY"])
	
	@commands.command(aliases=['weather'])
	async def w(self, ctx, location='台北市'):
		await ctx.channel.send("正如同**中央氣象局**曾經說過的")
		await ctx.channel.send(cwb(location, self.url))

async def setup(bot):
	await bot.add_cog(weather(bot))	