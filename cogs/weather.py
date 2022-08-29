import discord
import json
from discord.ext import commands
from core.classes import Cog_Extension
from core.cwb import cwb

class multi(Cog_Extension):	
	@commands.command(aliases=['weather'])
	async def w(self, message, location='台北市'):
		await message.channel.send("正如同**中央氣象局**曾經說過的")
		await message.channel.send(cwb(location))

def setup(bot):
	bot.add_cog(multi(bot))	