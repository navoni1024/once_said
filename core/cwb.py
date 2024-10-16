import requests

def cwb(location, url):
	orgData = requests.get(url, headers={'accept':'application/json'})
	data = orgData.json()

	if(location == "台北市"):
		location = "臺北市"
	if(location == "台北縣" or location == "臺北縣"):
		location = "新北市"

	forecastList = data["records"]["location"]
	forecast = None

	for i in forecastList:
		if(i["locationName"]==location):
			forecast = i
			break
	
	if(forecast == None):
		return "dafaq"
	
	
	result="**"+forecast["locationName"]
	result+= '**\n'
	result+= forecast["weatherElement"][0]["time"][2]["startTime"][:10]+' '
	result+= forecast["weatherElement"][0]["time"][2]["startTime"][11:16]
	result+= ' ~ '
	result+= forecast["weatherElement"][0]["time"][2]["endTime"][:10]+' '
	result+= forecast["weatherElement"][0]["time"][2]["endTime"][11:16]
	result+= '\n'
	result+= forecast["weatherElement"][0]["time"][2]["parameter"]["parameterName"]+' '
	result+= forecast["weatherElement"][1]["time"][2]["parameter"]["parameterName"]+"°C "

	return result

def req_quake_report(url):
	res = requests.get(url, headers={'accept':'application/json'})      
	quackData = res.json()
	return quackData['records']['Earthquake'][0]


def pack_quake_info():
	pass

