#!/usr/bin/python
# -*- coding: utf-8 -*- 

from parse_rest.connection import register
from parse_rest.datatypes import Object, GeoPoint

import json
import urllib2

APPLICATION_ID = "5fzYdG6YMpMPKBNSqvzhEL1OVoXgcVvlCAghW09Q"
REST_API_KEY = "3kxyAyfCh5CxEcCBJgw1e01FQMOue3zYGY9LYxyJ"

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

register(APPLICATION_ID, REST_API_KEY)

class TrashCanSTG(Object):
    pass

for key, value in dict.iteritems():

	url = root + value

	response = urllib2.urlopen(url).read().decode('utf8')

	data = json.loads(response)

	items = data["result"]["results"]

	for item in items:
		trashcanItem = TrashCanSTG(address=item[u'段、號及其他註明'], region=key, road=item[u'路名'], memo=item[u'備註'])
		trashcanItem.location = GeoPoint(latitude=float(item[u'緯度']), longitude=float(item[u'經度']))
		trashcanItem.save()


