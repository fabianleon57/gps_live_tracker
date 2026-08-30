import requests
import pandas as pd
from google.transit import gtfs_realtime_pb2

def get_bus_data(url, api_key):
	response=requests.get(url)
	content = response.content
	feed = gtfs_realtime_pb2.FeedMessage()
	feed.ParseFromString(content)

	bus_details = list()

	for entity in feed.entity:
	    if entity.HasField('vehicle'):
	        bus_id = entity.vehicle.vehicle.id
	        lat = entity.vehicle.position.latitude
	        lon = entity.vehicle.position.longitude
	        bus_details.append({'id' : bus_id, 'lat' : lat, 'lon' : lon})
	return bus_details

def get_bus_delay(url, api_key):
	response=requests.get(f'https://gtfsrt.prod.obanyc.com/tripUpdates?key={api_key}')
	content=response.content
	feed = gtfs_realtime_pb2.FeedMessage()
	feed.ParseFromString(content)

	bus_details = list()
	for entity in feed.entity:
		    if entity.HasField('trip_update'):
		        bus_details.append({'id' : entity.trip_update.vehicle.id, 'delay':  entity.trip_update.delay})
	return bus_details

def merge_bus_data(url, api_key):
	data  = get_bus_data(url, api_key)
	delay = get_bus_delay(url, api_key)
	merge = pd.merge(left=pd.DataFrame(data), right=pd.DataFrame(delay), on='id', how='left')
	merge.drop_duplicates(keep='first', inplace=True)
	merge_dict = merge.to_dict("records")
	return merge_dict
