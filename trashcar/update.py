#!/usr/bin/python
# -*- coding: utf-8 -*- 

from parse_rest.connection import register
from parse_rest.datatypes import Object


APPLICATION_ID = "nxkxfDhpFQBXOReTPFIPhGIaYowmT5uuscj3w3Kb"
REST_API_KEY = "6UXzStOsl61BtH2Y905HYkNDeObZ4iQqz0Pu1TRO"

register(APPLICATION_ID, REST_API_KEY)

class TPE201508(Object):
    pass

#filter
items = TPE201508.Query.filter(city='Taipei',foodscraps_wed='N')
items.limit(1000)

#update
for item in items:
	print item.address
	item.foodscraps_wed='Y'
	item.garbage_wed='Y'
	item.recycling_wed='Y'
	item.save()
