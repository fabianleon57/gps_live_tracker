import sys
from pathlib import Path

project_root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(project_root))

from main_functions import *

api_key = get_api_key(f'{os.getcwd()}/../api_keys/mta_api')
urlvehicle=f'https://gtfsrt.prod.obanyc.com/vehiclePositions?key={api_key}'
urldelay=f'https://gtfsrt.prod.obanyc.com/tripUpdates?key={api_key}'
bus_list = merge_bus_data(urlvehicle, urldelay, None)
gtfs_bus = merge_shapes_and_trips("data/MTA")
merged = bus_list.merge(gtfs_bus, on='route_id', how='left')
print(merged.head())