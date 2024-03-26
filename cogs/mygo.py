import cv2
import tempfile
import discord
import json
import tempfile
from discord.ext import commands
from core.classes import Cog_Extension
from core.video_processing import random_file, select_random_frame

with open('setting.json','r',encoding='utf8') as jfile:
	jdata = json.load(jfile)

class mygo(Cog_Extension):	
    @commands.command(aliases=['!!!!!'])
    async def mygo(self, message):    
        vid = random_file('./video')
        frame = select_random_frame(vid)
        temp_file = tempfile.mkstemp(suffix=".jpg")
        cv2.imwrite(temp_file[1], frame)
        await message.channel.send(file=discord.File(temp_file[1]))
        

def setup(bot):
	bot.add_cog(mygo(bot))


