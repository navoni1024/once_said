from discord.ext import commands
from core.search_channel import output_channel_list

class outputChannelList(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.settings = bot.settings

	@commands.command(aliases=['o'])
	async def outputChannelList(self, message):
		await output_channel_list(message)

async def setup(bot):
	await bot.add_cog(outputChannelList(bot))	