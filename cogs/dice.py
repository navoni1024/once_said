from discord.ext import commands
import random

class dice(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.settings = bot.settings
	
	@commands.command(aliases=['d', 'D'])
	async def dice(self, ctx, num):
		try:
			await ctx.channel.send(random.randint(1, int(num)))
		except:
			await ctx.channel.send("Error")
		
	@commands.command(aliases=['s', 'S'])
	async def select(self, ctx, *args):
		try:
			await ctx.channel.send(random.choice(args))
		except:
			await ctx.channel.send("Error")


async def setup(bot):
	await bot.add_cog(dice(bot))	