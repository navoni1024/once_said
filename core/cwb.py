from inspect import Parameter
import discord
import json
from discord.ext import commands
import requests

def cwb(location):
	url = "https://opendata.cwa.gov.tw/fileapi/v1/opendataapi/F-C0032-005?Authorization=CWB-8AA5A698-DA03-45A2-81E9-F45E7A8EABEF&downloadType=WEB&format=JSON"
	orgData = requests.get(url)
	data = orgData.json()

	if(location == "台北市"):
		location="臺北市"
	if(location == "台北縣" or location == "臺北縣"):
		location="新北市"

	forecastList = data["cwaopendata"]["dataset"]["location"]
	for i in forecastList:
		if(i["locationName"]==location):
			forecastList = i
			break
	
	try:
		tmp = forecastList["locationName"]
	except:
		return "dafaq"
	
	
	result="**"+forecastList["locationName"]
	result+= '**\n'
	result+= forecastList["weatherElement"][0]["time"][2]["startTime"][:10]+' '
	result+= forecastList["weatherElement"][0]["time"][2]["startTime"][11:16]
	result+= ' ~ '
	result+= forecastList["weatherElement"][0]["time"][2]["endTime"][:10]+' '
	result+= forecastList["weatherElement"][0]["time"][2]["endTime"][11:16]
	result+= '\n'
	result+= forecastList["weatherElement"][0]["time"][2]["parameter"]["parameterName"]+' '
	result+= forecastList["weatherElement"][1]["time"][2]["parameter"]["parameterName"]+"°C "

	return result

