import requests
from discord.ext import commands, tasks

PicURL = "https://cdn.discordapp.com/attachments/1082051109532749974/1290769989112168509/image0-9.gif?ex=670247fa&is=6700f67a&hm=2038b2a2e403dd4e477ed593f45283ed39d46f39e7ac53322d5701d80b8713b3&"

def pack_quack_info(QuackData):
    info = f"[地震速報 Earthquake Alert] {QuackData['ReportContent']}"
    return info

class earthquake(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.settings = bot.settings
        self.LastQuack = {}
        self.QuackCh = None
        self.url = f"https://opendata.cwa.gov.tw/api/v1/rest/datastore/E-A0015-001?Authorization={self.settings['API_KEY']}&limit=1"
        self.detector.start()

    def cog_unload(self):
        self.detector.cancel()

    @tasks.loop(seconds=30)
    async def detector(self):
        res = requests.get(self.url, headers={'accept':'application/json'})
        QuackData = res.json()
        if(self.LastQuack['EarthquakeNo'] != QuackData['records']['Earthquake'][0]['EarthquakeNo']):
            await self.QuackCh.send(PicURL)
            await self.QuackCh.send(pack_quack_info(self.LastQuack))
            await self.QuackCh.send(self.LastQuack['ReportImageURI'])
            self.LastQuack = QuackData['records']['Earthquake'][0]
         
    @detector.before_loop
    async def before_detector(self):     
        res = requests.get(self.url, headers={'accept':'application/json'})
        QuackData = res.json()
        self.LastQuack = QuackData['records']['Earthquake'][0]
        

    @commands.command(aliases=['test'])
    async def test_earthquake(self, message):
        #self.QuackCh = self.bot.get_channel(jdata["earthquake_channel"])
        self.QuackCh = message.channel
        await self.QuackCh.send(PicURL)
        await self.QuackCh.send(pack_quack_info(self.LastQuack))
        await self.QuackCh.send(self.LastQuack['ReportImageURI'])
		

async def setup(bot):
	await bot.add_cog(earthquake(bot))