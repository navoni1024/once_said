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
        self.LastQuack = None
        self.QuackCh = None

        self.SmallQuackURL = self.settings["small_felt_area_quake_url"].replace("API_KEY", self.settings["API_KEY"])
        self.RemarkableQuackURL = self.settings["small_felt_area_quake_url"].replace("API_KEY", self.settings["API_KEY"])

        self.detector.start()

    def cog_unload(self):
        self.detector.cancel()

    @tasks.loop(seconds=30)
    async def detector(self):
        res = requests.get(self.SmallQuackURL, headers={'accept':'application/json'})      
        SmallQuackData = res.json()

        res = requests.get(self.RemarkableQuackURL, headers={'accept':'application/json'})      
        RemarkableQuackData = res.json()
       
        if(self.LastQuack['EarthquakeNo'] != SmallQuackData['records']['Earthquake'][0]['EarthquakeNo'] and self.LastQuack['EarthquakeNo'] != RemarkableQuackData['records']['Earthquake'][0]['EarthquakeNo']):
            if(SmallQuackData['records']['Earthquake'][0]['EarthquakeNo'] > RemarkableQuackData['records']['Earthquake'][0]['EarthquakeNo']):
                self.LastQuack = SmallQuackData['records']['Earthquake'][0]
            else:
                self.LastQuack = RemarkableQuackData['records']['Earthquake'][0]
        
            await self.QuackCh.send(PicURL)
            await self.QuackCh.send(pack_quack_info(self.LastQuack))
            await self.QuackCh.send(self.LastQuack['ReportImageURI'])
                   
    @detector.before_loop
    async def before_detector(self):
        await self.bot.wait_until_ready()  
        res = requests.get(self.SmallQuackURL, headers={'accept':'application/json'})      
        SmallQuackData = res.json()

        res = requests.get(self.RemarkableQuackURL, headers={'accept':'application/json'})      
        RemarkableQuackData = res.json()
               
        if(SmallQuackData['records']['Earthquake'][0]['EarthquakeNo'] > RemarkableQuackData['records']['Earthquake'][0]['EarthquakeNo']):
            self.LastQuack = SmallQuackData['records']['Earthquake'][0]
        else:
            self.LastQuack = RemarkableQuackData['records']['Earthquake'][0]

        self.QuackCh = self.QuackCh = self.bot.get_channel(self.settings["earthquake_channel"])

    @commands.command(aliases=['test'])
    async def test_earthquake(self, ctx):
        #QuackCh = self.bot.get_channel(self.settings["earthquake_channel"])
        #self.QuackCh = ctx.channel
        await self.QuackCh.send(PicURL)
        await self.QuackCh.send(pack_quack_info(self.LastQuack))
        await self.QuackCh.send(self.LastQuack['ReportImageURI'])
		

async def setup(bot):
	await bot.add_cog(earthquake(bot))