from discord.ext import commands
import random

MAX_ROLLS = 20

class dice(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.settings = bot.settings
	
	@commands.command(aliases=['d', 'D'])
	async def dice(self, ctx, num):
		lower_bound = 1
		upper_bound = 1
		rolls = 1

		if ('-' in num and 'd' in num):
			random_range, rolls = num.split('d')
			lower_bound, upper_bound = map(int, random_range.split('-'))
			rolls = int(rolls)
		elif ('-' in num):
			lower_bound, upper_bound = map(int, num.split('-'))
			rolls = 1
		elif ('d' in num):
			upper_bound = int(num.split('d')[0])
			rolls = int(num.split('d')[1]) if 'd' in num else 1
		else:
			upper_bound = int(num)

		if (lower_bound > upper_bound or rolls < 1):
			await ctx.channel.send("Invaild range or rolls！")
		elif (rolls > MAX_ROLLS):
			await ctx.channel.send("Too many rolls!")
		else:
			result = ""
			for _ in range(rolls):
				result += str(random.randint(lower_bound, upper_bound))+' '
			await ctx.channel.send(result)

	@commands.command(aliases=['random_e', 'RE', 're'])
	async def random_emoji(self, ctx):
		emoji_list = ctx.guild.emojis
		selected_emoji = random.choice(emoji_list)
		await ctx.channel.send(selected_emoji)

	@commands.command(aliases=['s', 'S'])
	async def select(self, ctx, *args):
		try:
			await ctx.channel.send(random.choice(args))
		except:
			await ctx.channel.send("Error")

	@commands.command(aliases=['su', 'SU'])
	async def select_user(self, ctx):
		roles = ctx.message.role_mentions
		await ctx.channel.send(str(roles[0].members))
		members = []
		for i in roles:
			members.extend(i.members)
		members = set(members)

		if not members:
			await ctx.channel.send("No members found in the mentioned roles.")
			return

		selected_user = random.choice(members)
		await ctx.channel.send(selected_user.name)

async def setup(bot):
	await bot.add_cog(dice(bot))	