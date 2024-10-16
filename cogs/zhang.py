import discord
import tempfile
import os
from discord.ext import commands
from core.video_processing import random_frame, random_gif

class zhang(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.settings = bot.settings

    @commands.command(aliases=['z'])
    async def zhang(self, ctx):
        vid = self.settings["zhang_path"]
        temp_file = tempfile.mkstemp(suffix=".png")
        random_frame(vid, temp_file[1])
        await ctx.channel.send(file=discord.File(temp_file[1]))
        os.close(temp_file[0])
        os.unlink(temp_file[1])

    @commands.command(aliases=['zG', 'zg'])
    async def zhang_gif(self, ctx, duration=3.0):
        if(duration <= 0):
            await ctx.channel.send("The requested GIF length is invalid")
            return
        if(duration > self.settings['gif_duration_limit']):
            await ctx.channel.send("The requested GIF length is too long")
            return
        
        hint = await ctx.channel.send("generating...")
        vid = self.settings["zhang_path"]
        temp_file = tempfile.mkstemp(suffix=".gif")
        random_gif(vid, temp_file[1], duration)
        await ctx.channel.send(file=discord.File(temp_file[1]))
        os.close(temp_file[0])
        os.unlink(temp_file[1])
        await hint.delete()   

async def setup(bot):
	await bot.add_cog(zhang(bot))	
