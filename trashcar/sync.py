#!/usr/bin/python
# -*- coding: utf-8 -*- 

from parse_rest.connection import register
from parse_rest.datatypes import Object, GeoPoint
from parse_rest.connection import ParseBatcher


import json,httplib
import urllib2
import geocoder

APPLICATION_ID = "nxkxfDhpFQBXOReTPFIPhGIaYowmT5uuscj3w3Kb"
REST_API_KEY = "6UXzStOsl61BtH2Y905HYkNDeObZ4iQqz0Pu1TRO"

url = 'http://data.ntpc.gov.tw/od/data/api/28AB4122-60E1-4065-98E5-ABCCB69AACA6?$format=json'

register(APPLICATION_ID, REST_API_KEY)

class RealTime(Object):
    pass

class RealTime_STG2(Object):
    pass


response = urllib2.urlopen(url).read().decode('utf8')

data = json.loads(response)

items = data

#delete stg record
realtime = RealTime_STG2.Query.all()
realtime.limit(1000)
batcher = ParseBatcher()
batcher.batch_delete(realtime)

#import data to stg
for item in items:
	g = geocoder.google(item['location'])
	trashcanItem = RealTime_STG2(lineid=item['lineid'], address=item['location'], carno=item['car'], cartime=item['time'])
	trashcanItem.location = GeoPoint(latitude=float(g.lat), longitude=float(g.lng))
	trashcanItem.save()

#delete target record
realtime = RealTime.Query.all()
realtime.limit(1000)
batcher = ParseBatcher()
batcher.batch_delete(realtime)

#import data to target
rec = RealTime_STG2.Query.all()
rec.limit(1000)
for d in rec:
	item = RealTime(lineid=d.lineid, address=d.address, carno=d.carno, cartime=d.cartime)
	item.location = d.location
	item.save()


