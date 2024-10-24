import requests
from datetime import datetime

def parse_time(time_str):
    return datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")

def req_quake_report(url):
	res = requests.get(url, headers={'accept':'application/json'})      
	quackData = res.json()
	return quackData['records']['Earthquake'][0]

SmallQuackData = req_quake_report("https://opendata.cwa.gov.tw/api/v1/rest/datastore/E-A0016-001?Authorization=CWA-236518FC-3430-44A7-B33A-992E3C872BF2&limit=1")
RemarkableQuackData = req_quake_report("https://opendata.cwa.gov.tw/api/v1/rest/datastore/E-A0015-001?Authorization=CWA-236518FC-3430-44A7-B33A-992E3C872BF2&limit=1")

if(parse_time(SmallQuackData['EarthquakeInfo']['OriginTime']) > parse_time(RemarkableQuackData['EarthquakeInfo']['OriginTime'])):
    LastQuack = SmallQuackData
else:
    LastQuack = RemarkableQuackData

print(LastQuack['ReportContent'])