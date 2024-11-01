import discord
import datetime
import os
from discord.ext import commands, tasks

tz = datetime.timezone(datetime.timedelta(hours=8))
time = datetime.time(hour=22, minute=00, tzinfo=tz)

PicDict = "./asset/"
checkChID = 1239920756624719892
checkImage = discord.File(os.path.join(PicDict, "nCheck.jpg"))

class check(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.settings = bot.settings
        self.checkCh = None
        self.check.start()

    def cog_unload(self):
        self.detector.cancel()
    
    @tasks.loop(time=time)
    async def check(self):
        await self.checkCh.send(f"Day {str(datetime.datetime.now(tz).day)}:", file=checkImage)

    @check.before_loop
    async def before_detector(self):
        self.checkCh = await self.bot.fetch_channel(int(checkChID))

    @commands.command(aliases=['test_nnn', 'test_NNN'])
    async def test_nCheck(self, ctx):
        await self.bot.wait_until_ready()
        await self.checkCh.send(f"Day {str(datetime.datetime.now(tz).day)}:", file=checkImage)

async def setup(bot):
	await bot.add_cog(check(bot))