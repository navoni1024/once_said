import discord
from discord.ext import commands
import json
import os
import asyncio
import logging

with open('setting_test.json','r',encoding='utf8') as jfile:
	jdata = json.load(jfile)

async def load_extensions():
	for filename in os.listdir('./cogs'):
		if filename.endswith('.py'):
			await bot.load_extension(f'cogs.{filename[:-3]}')
	await bot.start(jdata['token'])

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
discord.utils.setup_logging(handler=handler)

bot = commands.Bot(commands.when_mentioned_or("peko"), intents=intents)
bot.settings = jdata

@bot.event
async def on_ready():
	print('\\ONCE_SAID ON/')

@bot.command()
async def MUR(ctx):
    await ctx.send("Test command is working!")

asyncio.run(load_extensions())



"""
if __name__ == "__main__":
	bot.run(jdata['token'])
"""