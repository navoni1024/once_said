from inspect import Parameter
import discord
import json
from discord.ext import commands
import requests

def cwb(location):
	with open('weather.json','r',encoding='utf8') as jfile:
			jdata = json.load(jfile)
	try:
		url = jdata[location]
	except:
		return "dafaq"
	orgData = requests.get(url)
	data = orgData.json()
	forecastList =  data['cwbopendata']['dataset']['parameterSet']['parameter']
	f = ''
	for i in forecastList:
		f = f+i['parameterValue']
	return f