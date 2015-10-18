#!/usr/bin/python
# -*- coding: utf-8 -*- 

from parse_rest.connection import register
from parse_rest.datatypes import Object, GeoPoint
from parse_rest.connection import ParseBatcher


import json,httplib
import urllib2


APPLICATION_ID = "6M0xS8A8uaqXbGGP8GAVFCw8ah7B6cif0NlZhYm6"
REST_API_KEY = "ASDpoFdwFAdbRlI6bAH7X0onYK5xuE8XWwL9uafm"

urlTaipei = 'http://data.taipei/opendata/datalist/apiAccess?scope=resourceAquire&rid=8f2e2264-6eab-451f-a66d-34aa2a0aa7b1'
urlNewTaipei = 'http://data.ntpc.gov.tw/od/data/api/EDC3AD26-8AE7-4916-A00B-BC6048D19BF8?$format=json'

register(APPLICATION_ID, REST_API_KEY)

class TruckSTG(Object):
    pass

## Taipei
response = urllib2.urlopen(urlTaipei).read().decode('utf8')

data = json.loads(response)

items = data["result"]["results"]

#import data
for item in items:
	#print item['CarTime'],item['CarTime'][0:item['CarTime'].index(':')]
	#print item['Address'],item['CarTime'],item['Region'],item['Li'],item['Lat'],item['Lng']

	carTime=item['CarTime'].replace(u'：',':')
	strHour=carTime[0:carTime.index(':')]

	truck=TruckSTG(city='Taipei',region=item['Li'],address=item['Address'],lineid='',line=item['CarNumber'],carno=item['CarNo']
		,time=item['CarTime'],hour=strHour,memo=item['DepName']
		,garbage_sun='N',garbage_mon='Y',garbage_tue='Y',garbage_wed='N',garbage_thu='Y',garbage_fri='Y',garbage_sat='Y'
		,recycling_sun='N',recycling_mon='Y',recycling_tue='Y',recycling_wed='N',recycling_thu='Y',recycling_fri='Y',recycling_sat='Y'
		,foodscraps_sun='N',foodscraps_mon='Y',foodscraps_tue='Y',foodscraps_wed='N',foodscraps_thu='Y',foodscraps_fri='Y',foodscraps_sat='Y')
	truck.location = GeoPoint(latitude=float(item['Lat']), longitude=float(item['Lng']))
	truck.save()



# New Taipei
response = urllib2.urlopen(urlNewTaipei).read().decode('utf8')

data = json.loads(response)

items = data

#import data
for item in items:
	#print item['name'],item['time'],item['time'][0:item['time'].index(':')]
	#print item['Address'],item['CarTime'],item['Region'],item['Li'],item['Lat'],item['Lng']
	
	truck=TruckSTG(city='NewTaipei',region=item['village'],address=item['name'],lineid=item['lineid']
		,line=item['linename'],carno=item['rank'],time=item['time'],hour=item['time'][0:item['time'].index(':')],memo=item['memo']
		,garbage_sun=(item['garbage_sun'] if item['garbage_sun']=='Y' else 'N')
		,garbage_mon=(item['garbage_mon'] if item['garbage_mon']=='Y' else 'N')
		,garbage_tue=(item['garbage_tue'] if item['garbage_tue']=='Y' else 'N')
		,garbage_wed=(item['garbage_wed'] if item['garbage_wed']=='Y' else 'N')
		,garbage_thu=(item['garbage_thu'] if item['garbage_thu']=='Y' else 'N')
		,garbage_fri=(item['garbage_fri'] if item['garbage_fri']=='Y' else 'N')
		,garbage_sat=(item['garbage_sat'] if item['garbage_sat']=='Y' else 'N')
		,recycling_sun=(item['recycling_sun'] if item['recycling_sun']=='Y' else 'N')
		,recycling_mon=(item['recycling_mon'] if item['recycling_mon']=='Y' else 'N')
		,recycling_tue=(item['recycling_tue'] if item['recycling_tue']=='Y' else 'N')
		,recycling_wed=(item['recycling_wed'] if item['recycling_wed']=='Y' else 'N')
		,recycling_thu=(item['recycling_thu'] if item['recycling_thu']=='Y' else 'N')
		,recycling_fri=(item['recycling_fri'] if item['recycling_fri']=='Y' else 'N')
		,recycling_sat=(item['recycling_sat'] if item['recycling_sat']=='Y' else 'N')
		,foodscraps_sun=(item['foodscraps_sun'] if item['foodscraps_sun']=='Y' else 'N')
		,foodscraps_mon=(item['foodscraps_mon'] if item['foodscraps_mon']=='Y' else 'N')
		,foodscraps_tue=(item['foodscraps_tue'] if item['foodscraps_tue']=='Y' else 'N')
		,foodscraps_wed=(item['foodscraps_wed'] if item['foodscraps_wed']=='Y' else 'N')
		,foodscraps_thu=(item['foodscraps_thu'] if item['foodscraps_thu']=='Y' else 'N')
		,foodscraps_fri=(item['foodscraps_fri'] if item['foodscraps_fri']=='Y' else 'N')
		,foodscraps_sat=(item['foodscraps_sat'] if item['foodscraps_sat']=='Y' else 'N'))
	
	truck.location = GeoPoint(latitude=float(item['latitude']), longitude=float(item['longitude']))
	truck.save()
