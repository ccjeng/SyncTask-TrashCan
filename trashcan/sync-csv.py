#!/usr/bin/python
# -*- coding: utf-8 -*- 

import codecs, json,httplib
import urllib2
import ast

root = 'http://data.taipei/opendata/datalist/apiAccess?scope=resourceAquire&rid='

dict = {u'士林區':'97cc923a-e9ee-4adc-8c3d-335567dc15d3'
,u'大同區':'5fa14e06-018b-4851-8316-1ff324384f79'
,u'大安區':'f40cd66c-afba-4409-9289-e677b6b8d00e'
,u'中山區':'33b2c4c5-9870-4ee9-b280-a3a297c56a22'
,u'中正區':'0b544701-fb47-4fa9-90f1-15b1987da0f5'
,u'內湖區':'37eac6d1-6569-43c9-9fcf-fc676417c2cd'
,u'文山區':'46647394-d47f-4a4d-b0f0-14a60ac2aade'
,u'北投區':'05d67de9-a034-4177-9f53-10d6f79e02cf'
,u'松山區':'179d0fe1-ef31-4775-b9f0-c17b3adf0fbc'
,u'信義區':'8cbb344b-83d2-4176-9abd-d84508e7dc73'
,u'南港區':'7b955414-f460-4472-b1a8-44819f74dc86'
,u'萬華區':'5697d81f-7c9d-43fc-a202-ae8804bbd34b'
}

class TrashCan(object):
    def __init__(self, address, region, road, memo, location):
    	self.address = address
    	self.region = region
    	self.road = road
    	self.memo = memo
    	self.location = location

class Location(object):
	def __init__(self, latitude, longitude):
		self.latitude = latitude
		self.longitude = longitude

TrashCans = []

for key, value in dict.iteritems():

	url = root + value

	print key

	response = urllib2.urlopen(url).read().decode('utf8')

	data = json.loads(response)

	items = data["result"]["results"]

	for item in items:
		locationString=ast.literal_eval('{"__type": "GeoPoint", "longitude":' + str(float(item[u'經度'])) + ',"latitude":' + str(float(item[u'緯度'])) + ' }')
	
		t = TrashCan(item[u'段、號及其他註明']
			,key
			,item[u'路名']
			,item[u'備註']
			,locationString)

		jsonStringTruck = json.dumps(t.__dict__, ensure_ascii=False)
		TrashCans.append(ast.literal_eval(jsonStringTruck))

json_string = '{"results":' + json.dumps(TrashCans, ensure_ascii=False) + '}'

with codecs.open("Bin.json", "w") as outfile:
	outfile.write(json_string)
