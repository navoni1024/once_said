import discord
import logging
import json
import os
from discord.ext import commands

with open('setting.json','r',encoding='utf8') as jfile:
	jdata = json.load(jfile)

bot = commands.Bot(command_prefix=commands.when_mentioned_or(jdata['prefix']))

for filename in os.listdir('./cogs'):
	if filename.endswith('.py'):
		bot.load_extension(f'cogs.{filename[:-3]}')

@bot.event
async def on_ready():
	print('\ONCE_SAID ON/')
	
@bot.command()
async def load(ctx, cog_name):
	try:
		bot.load_extension(f'cogs.{cog_name}')
	except:
		await ctx.send('Failed.')
		return
	await ctx.send('load success!')

@bot.command()
async def unload(ctx, cog_name):
	try:
		bot.unload_extension(f'cogs.{cog_name}')
	except:
		await ctx.send('Failed.')
		return
	await ctx.send('unload success!')

@bot.command()
async def reload(ctx, cog_name):
	try:
		bot.reload_extension(f'cogs.{cog_name}')
	except:
		await ctx.send('Failed.')
		return
	await ctx.send('reload success!')

if __name__ == "__main__":
	bot.run(jdata['token'])
