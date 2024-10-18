import requests
import os
import discord
from datetime import datetime
from discord.ext import commands, tasks
from core.cwb import req_quake_report

PicDict = "./asset/"

async def send_quack_info(QuackData, QuackCh):

    pic = os.path.join(PicDict, "sweetCamper.gif")
    
    if("花蓮" in QuackData["EarthquakeInfo"]["Epicenter"]["Location"]):
        pic = os.path.join(PicDict, "Hua_king.jpg")
    
    pic = discord.File(pic)
    info = f"[地震速報 Earthquake Alert] {QuackData['ReportContent']}"

    await QuackCh.send(file=pic)
    await QuackCh.send(info)
    await QuackCh.send(QuackData['ReportImageURI'])
    

def parse_time(time_str):
    return datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")

class earthquake(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.settings = bot.settings
        self.LastQuack = None
        self.QuackCh = None

        self.SmallQuackURL = self.settings["small_felt_area_quake_url"].replace("API_KEY", self.settings["API_KEY"])
        self.RemarkableQuackURL = self.settings["small_felt_area_quake_url"].replace("API_KEY", self.settings["API_KEY"])

        self.detector.start()

    def cog_unload(self):
        self.detector.cancel()

    @tasks.loop(seconds=15)
    async def detector(self):
        SmallQuackData = req_quake_report(self.SmallQuackURL)
        RemarkableQuackData = req_quake_report(self.RemarkableQuackURL)
       
        if(parse_time(SmallQuackData['EarthquakeInfo']['OriginTime']) > parse_time(RemarkableQuackData['EarthquakeInfo']['OriginTime'])):
            NewQuack = SmallQuackData
        else:
            NewQuack = RemarkableQuackData

        if(parse_time(NewQuack['EarthquakeInfo']['OriginTime']) > parse_time(self.LastQuack['EarthquakeInfo']['OriginTime'])):
            self.LastQuack = NewQuack
            await send_quack_info(self.LastQuack, self.QuackCh)
                   
    @detector.before_loop
    async def before_detector(self):
        SmallQuackData = req_quake_report(self.SmallQuackURL)
        RemarkableQuackData = req_quake_report(self.RemarkableQuackURL)
       
        if(parse_time(SmallQuackData['EarthquakeInfo']['OriginTime']) > parse_time(RemarkableQuackData['EarthquakeInfo']['OriginTime'])):
            self.LastQuack = SmallQuackData
        else:
            self.LastQuack = RemarkableQuackData
        
        await self.bot.wait_until_ready()
        self.QuackCh = self.bot.get_channel(int(self.settings["earthquake_channel"]))
            

    @commands.command(aliases=['test'])
    async def test_earthquake(self, ctx):
        #QuackCh = self.bot.get_channel(self.settings["earthquake_channel"])
        #self.QuackCh = ctx.channel
        await self.bot.wait_until_ready()
        await send_quack_info(self.LastQuack, self.QuackCh)

async def setup(bot):
	await bot.add_cog(earthquake(bot))