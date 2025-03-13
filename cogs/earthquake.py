import requests
import os
import discord
import tempfile
from io import BytesIO
from PIL import Image
from discord.ext import commands, tasks
from core.cwb import req_quake_report, parse_time

PicDict = "./asset/"

def image_composite(base_image, overlay, output_path, position='right'):

    if not isinstance(base_image, Image.Image):
        base_image = Image.open(base_image)
    if not isinstance(overlay, Image.Image):
        overlay = Image.open(overlay)

    max_size = (200, 400)
    coord = (688-10, 866-10)

    if(position=='left'):
        max_size = (150, 200)
        coord = (60, 570)

    overlay.thumbnail(max_size)
    overlay_width, overlay_height = overlay.size
    position = (coord[0] - overlay_width, coord[1] - overlay_height)

    base_image.paste(overlay, position)  
    base_image.save(output_path)

async def send_quack_info(QuackData, QuackCh):

    pic = os.path.join(PicDict, "sweetCamper.gif")
    response = requests.get(QuackData['ReportImageURI'])
    ReprotImage = Image.open(BytesIO(response.content))
    info = f"[地震速報 Earthquake Alert] {QuackData['ReportContent']}"
    
    if("花蓮" in QuackData["EarthquakeInfo"]["Epicenter"]["Location"]):    
        temp_file = tempfile.mkstemp(suffix=".png")

        if(int(QuackData["EarthquakeInfo"]["EarthquakeMagnitude"]["MagnitudeValue"]) >= 5):
            image_composite(ReprotImage, os.path.join(PicDict, "Hua_king.jpg"), temp_file[1])
        else:
            image_composite(ReprotImage, os.path.join(PicDict, "Hua_king2.jpg"), temp_file[1])

        ReprotImage = discord.File(temp_file[1])
        
        await QuackCh.send(info)
        await QuackCh.send(file=ReprotImage)
        os.close(temp_file[0])
        os.unlink(temp_file[1])
    
    elif("嘉義" in QuackData["EarthquakeInfo"]["Epicenter"]["Location"]):    
        temp_file = tempfile.mkstemp(suffix=".png")
        image_composite(ReprotImage, os.path.join(PicDict, "cha.png"), temp_file[1])
        ReprotImage = discord.File(temp_file[1])
        
        await QuackCh.send(info)
        await QuackCh.send(file=ReprotImage)
        os.close(temp_file[0])
        os.unlink(temp_file[1])

    elif("宜蘭" in QuackData["EarthquakeInfo"]["Epicenter"]["Location"]):    
        temp_file = tempfile.mkstemp(suffix=".png")
        image_composite(ReprotImage, os.path.join(PicDict, "yilan.png"), temp_file[1])
        ReprotImage = discord.File(temp_file[1])
        
        await QuackCh.send(info)
        await QuackCh.send(file=ReprotImage)
        os.close(temp_file[0])
        os.unlink(temp_file[1])

    elif("臺東" in QuackData["EarthquakeInfo"]["Epicenter"]["Location"]):    
        temp_file = tempfile.mkstemp(suffix=".png")
        image_composite(ReprotImage, os.path.join(PicDict, "Xiaomi_9.png"), temp_file[1])
        ReprotImage = discord.File(temp_file[1])
        
        await QuackCh.send(info)
        await QuackCh.send(file=ReprotImage)
        os.close(temp_file[0])
        os.unlink(temp_file[1])

    else:
        temp_file = tempfile.mkstemp(suffix=".png")
        ReprotImage.save(temp_file[1])
        await QuackCh.send(file=discord.File(pic))
        await QuackCh.send(info)
        await QuackCh.send(file=discord.File(temp_file[1]))
        os.close(temp_file[0])
        os.unlink(temp_file[1])

class earthquake(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.settings = bot.settings
        self.LastQuack = None
        self.QuackCh = None

        self.SmallQuackURL = self.settings["small_felt_area_quake_url"].replace("API_KEY", self.settings["API_KEY"])
        self.RemarkableQuackURL = self.settings["remarkable_earthquake_url"].replace("API_KEY", self.settings["API_KEY"])

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