import requests
from datetime import datetime
from discord.ext import commands, tasks
from core.cwb import req_quake_report

PicURL = "https://cdn.discordapp.com/attachments/1082051109532749974/1290769989112168509/image0-9.gif?ex=670247fa&is=6700f67a&hm=2038b2a2e403dd4e477ed593f45283ed39d46f39e7ac53322d5701d80b8713b3&"

def pack_quack_info(QuackData):
    info = f"[地震速報 Earthquake Alert] {QuackData['ReportContent']}"
    return info

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
            await self.QuackCh.send(PicURL)
            await self.QuackCh.send(pack_quack_info(self.LastQuack))
            await self.QuackCh.send(self.LastQuack['ReportImageURI'])

                   
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
        await self.QuackCh.send(PicURL)
        await self.QuackCh.send(pack_quack_info(self.LastQuack))
        await self.QuackCh.send(self.LastQuack['ReportImageURI'])
		

async def setup(bot):
	await bot.add_cog(earthquake(bot))