#!/usr/bin/python
# -*- coding: utf-8 -*-

import codecs, json
import requests
import ast

def checkCarTimeValue(time, num):
	if '-' in time:
		time = time.split('-')[num]
	else:
		if '~' in time:
			time = time.split('~')[num]
	time = time.replace('：', '').replace(':','')
	try:
		val = int(time)
	except ValueError:
		print("not an int! "  + time)

urlTaipei = 'http://data.taipei/opendata/datalist/apiAccess?scope=resourceAquire&rid=8f2e2264-6eab-451f-a66d-34aa2a0aa7b1'
urlNewTaipei = 'http://data.ntpc.gov.tw/od/data/api/EDC3AD26-8AE7-4916-A00B-BC6048D19BF8?$format=json'

urlNewTaipeiList = ['&$top=2000' #1~2000
, '&$top=2000&$skip=2000' #2000~4000
, '&$top=2000&$skip=4000' #4000~6000
, '&$top=2000&$skip=6000'
, '&$top=2000&$skip=8000'
, '&$top=2000&$skip=10000'
, '&$top=2000&$skip=12000'
, '&$top=2000&$skip=14000'
, '&$top=2000&$skip=16000'
, '&$top=2000&$skip=18000'
, '&$top=2000&$skip=20000'
, '&$top=2000&$skip=22000'
, '&$top=2000&$skip=24000'
, '&$top=2000&$skip=26000'
, '&$top=2000&$skip=28000'
, '&$top=2000&$skip=30000' #30000~32000
]


class Truck(object):
    def __init__(self, city, region, address, lineid, line, carno, time, hour, memo
    	, garbage_sun, garbage_mon, garbage_tue, garbage_wed, garbage_thu, garbage_fri, garbage_sat
    	, recycling_sun, recycling_mon, recycling_tue, recycling_wed, recycling_thu, recycling_fri, recycling_sat
    	, foodscraps_sun, foodscraps_mon, foodscraps_tue, foodscraps_wed, foodscraps_thu, foodscraps_fri, foodscraps_sat
    	, sun, mon, tue, wed, thu, fri, sat
    	, location
    	):
        self.city = city
        self.region = region
        self.address = address
        self.lineid = lineid
        self.line = line
        self.carno = carno
        self.time = time
        self.hour = hour
        self.memo = memo
        self.garbage_sun = garbage_sun
        self.garbage_mon = garbage_mon
        self.garbage_tue = garbage_tue
        self.garbage_wed = garbage_wed
        self.garbage_thu = garbage_thu
        self.garbage_fri = garbage_fri
        self.garbage_sat = garbage_sat
        self.recycling_sun = recycling_sun
        self.recycling_mon = recycling_mon
        self.recycling_tue = recycling_tue
        self.recycling_wed = recycling_wed
        self.recycling_thu = recycling_thu
        self.recycling_fri = recycling_fri
        self.recycling_sat = recycling_sat
        self.foodscraps_sun = foodscraps_sun
        self.foodscraps_mon = foodscraps_mon
        self.foodscraps_tue = foodscraps_tue
        self.foodscraps_wed = foodscraps_wed
        self.foodscraps_thu = foodscraps_thu
        self.foodscraps_fri = foodscraps_fri
        self.foodscraps_sat = foodscraps_sat
        self.sun = sun
        self.mon = mon
        self.tue = tue
        self.wed = wed
        self.thu = thu
        self.fri = fri
        self.sat = sat
        self.location = location

class Location(object):
	def __init__(self, latitude, longitude):
		self.latitude = latitude
		self.longitude = longitude

Trucks = []

count = 0;

## Taipei
print(urlTaipei)
response = requests.get(urlTaipei)
items = response.json()["result"]["results"]

for item in items:
	count = count + 1;
	carTime=item['CarTime'].replace(u'：',':')
	strHour=str(int(carTime[0:carTime.index(':')]))
	locationString=ast.literal_eval('{"__type": "GeoPoint", "longitude":' + str(float(item['Lng'])) + ',"latitude":' + str(float(item['Lat'])) + ' }')
	timeString=item['CarTime'].replace(' ','').replace('(一.五各收1次)','')

	#verfy time format
	checkCarTimeValue(timeString,0)
	checkCarTimeValue(timeString,1)
	t = Truck('Taipei',item['Address'][3:6] #,item['Region']
		,item['Address'],'',item['CarNo'],item['CarNumber'],timeString,strHour,''
		,'N','Y','Y','N','Y','Y','Y'
		,'N','Y','Y','N','Y','Y','Y'
		,'N','Y','Y','N','Y','Y','Y'
		,'N','Y','Y','N','Y','Y','Y'
		, locationString
		)
	jsonStringTruck = json.dumps(t.__dict__, ensure_ascii=False)
	Trucks.append(ast.literal_eval(jsonStringTruck))

# New Taipei
for top in urlNewTaipeiList:
	url = urlNewTaipei + top
	print(url)
	response = requests.get(url)
	items = response.json()

	#import data
	for item in items:
		count = count + 1;
		strHour=str(int(item['time'][0:item['time'].index(':')]))

		longitude=float(item['longitude'])
		latitude=float(item['latitude'])
		#Fix error location data

		if latitude>100:
			longitude=float(item['latitude'])
			latitude=float(item['longitude'])
			print(item['village']+' '+item['time']+ ' ' +str(longitude) + ' ' + str(latitude))

		locationString=ast.literal_eval('{"__type": "GeoPoint", "longitude":' + str(longitude) + ',"latitude":' + str(latitude) + ' }')


		if item['garbage_sun'] == 'Y' or item['recycling_sun'] == 'Y' or item['foodscraps_sun'] == 'Y':
			sun = 'Y'
		else:
			sun = 'N'

		if item['garbage_mon'] == 'Y' or item['recycling_mon'] == 'Y' or item['foodscraps_mon'] == 'Y':
			mon = 'Y'
		else:
		 	mon = 'N'

		if item['garbage_tue'] == 'Y' or item['recycling_tue'] == 'Y' or item['foodscraps_tue'] == 'Y':
			tue = 'Y'
		else:
			tue = 'N'

		if item['garbage_wed'] == 'Y' or item['recycling_wed'] == 'Y' or item['foodscraps_wed'] == 'Y':
			wed = 'Y'
		else:
			wed = 'N'

		if item['garbage_thu'] == 'Y' or item['recycling_thu'] == 'Y' or item['foodscraps_thu'] == 'Y':
			thu = 'Y'
		else:
			thu = 'N'

		if item['garbage_fri'] == 'Y' or item['recycling_fri'] == 'Y' or item['foodscraps_fri'] == 'Y':
			fri = 'Y'
		else:
		 	fri = 'N'

		if item['garbage_sat'] == 'Y' or item['recycling_sat'] == 'Y' or item['foodscraps_sat'] == 'Y':
			sat = 'Y'
		else:
			sat = 'N'

		#verfy time format
		checkCarTimeValue(item['time'],0)
		checkCarTimeValue(item['time'],1)

		t = Truck('NewTaipei',item['city'],item['name'],item['lineid'],item['linename'],item['rank'],item['time'],strHour,item['memo']
			,(item['garbage_sun'] if item['garbage_sun']=='Y' else 'N')
			,(item['garbage_mon'] if item['garbage_mon']=='Y' else 'N')
			,(item['garbage_tue'] if item['garbage_tue']=='Y' else 'N')
			,(item['garbage_wed'] if item['garbage_wed']=='Y' else 'N')
			,(item['garbage_thu'] if item['garbage_thu']=='Y' else 'N')
			,(item['garbage_fri'] if item['garbage_fri']=='Y' else 'N')
			,(item['garbage_sat'] if item['garbage_sat']=='Y' else 'N')
			,(item['recycling_sun'] if item['recycling_sun']=='Y' else 'N')
			,(item['recycling_mon'] if item['recycling_mon']=='Y' else 'N')
			,(item['recycling_tue'] if item['recycling_tue']=='Y' else 'N')
			,(item['recycling_wed'] if item['recycling_wed']=='Y' else 'N')
			,(item['recycling_thu'] if item['recycling_thu']=='Y' else 'N')
			,(item['recycling_fri'] if item['recycling_fri']=='Y' else 'N')
			,(item['recycling_sat'] if item['recycling_sat']=='Y' else 'N')
			,(item['foodscraps_sun'] if item['foodscraps_sun']=='Y' else 'N')
			,(item['foodscraps_mon'] if item['foodscraps_mon']=='Y' else 'N')
			,(item['foodscraps_tue'] if item['foodscraps_tue']=='Y' else 'N')
			,(item['foodscraps_wed'] if item['foodscraps_wed']=='Y' else 'N')
			,(item['foodscraps_thu'] if item['foodscraps_thu']=='Y' else 'N')
			,(item['foodscraps_fri'] if item['foodscraps_fri']=='Y' else 'N')
			,(item['foodscraps_sat'] if item['foodscraps_sat']=='Y' else 'N')
			,sun
			,mon
			,tue
			,wed
			,thu
			,fri
			,sat
			,locationString
			)
		jsonStringTruck = json.dumps(t.__dict__, ensure_ascii=False)
		Trucks.append(ast.literal_eval(jsonStringTruck))


print('Total Count = ' + str(count))

json_string = '{"results":' + json.dumps(Trucks, ensure_ascii=False) + '}'


#Write to Json File
with codecs.open("TPE20160911.json", "w") as outfile:
	outfile.write(json_string)
	#outfile.write(json_string.decode('utf8'))
	#json_string #.decode('unicode-escape').encode('utf8')


