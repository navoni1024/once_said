import discord
import json
import os
import asyncio
from discord.ext import commands

async def load_extensions():
	for filename in os.listdir('./cogs'):
		if filename.endswith('.py'):
			await bot.load_extension(f'cogs.{filename[:-3]}')
	await bot.start(jdata['token'])

with open('setting.json','r',encoding='utf8') as jfile:
	jdata = json.load(jfile)

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix=commands.when_mentioned_or(jdata['prefix']), intents=intents)
bot.settings = jdata

asyncio.run(load_extensions())

@bot.event
async def on_ready():
	print('\ONCE_SAID ON/')

"""
if __name__ == "__main__":
	bot.run(jdata['token'])
"""