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
	
	location = forecast["locationName"]
	result = f"**{location}**"

	for i in range(3):
		start_time = forecast["weatherElement"][0]["time"][i]["startTime"]
		end_time = forecast["weatherElement"][0]["time"][i]["endTime"]
		weather = forecast["weatherElement"][0]["time"][i]["parameter"]["parameterName"]
		pop = forecast["weatherElement"][1]["time"][i]["parameter"]["parameterName"] + "%"
		min_temp = forecast["weatherElement"][2]["time"][i]["parameter"]["parameterName"] + "°C"
		max_temp = forecast["weatherElement"][4]["time"][i]["parameter"]["parameterName"] + "°C"
		feel = forecast["weatherElement"][3]["time"][i]["parameter"]["parameterName"]

		result += f"\n{start_time} 至 {end_time}\n"
		result += f"    天氣狀況：{weather}\n"
		result += f"    降雨機率：{pop}\n"
		result += f"    最低溫度：{min_temp}\n"
		result += f"    最高溫度：{max_temp}\n"
		result += f"    體感：{feel}\n"
    
	return result

def req_quake_report(url):
	res = requests.get(url, headers={'accept':'application/json'})      
	quackData = res.json()
	return quackData['records']['Earthquake'][0]


def pack_quake_info():
	pass

