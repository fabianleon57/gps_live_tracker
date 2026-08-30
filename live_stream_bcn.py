#!/Users/fabiandeleon/.pyenv/shims/python
import folium
import sys
import streamlit as st
import time
import pydeck as pdk
import pandas as pd
from streamlit_folium import st_folium
from main_functions import *

st.set_page_config(page_title="MTA Live Bus Tracker", layout="wide")

api_key='2fcc6aee-7345-4499-aee3-bdcd1087bc00'
url=f'https://gtfsrt.prod.obanyc.com/vehiclePositions?key={api_key}'

VIEW_STATE = pdk.ViewState(
    latitude=40.7128,
    longitude=-74.0060,
    zoom=12,
    pitch=0
)



map_placeholder = st.empty()
REFRESH_INTERVAL_SECS = 30
#nyc_map = folium.Map(location=[40.7646, -73.9798], zoom_start=14, tiles="CartoDB positron")
bus_details = get_bus_data(url, api_key)

df = pd.DataFrame(bus_details)  # Required columns: 'lat', 'lon', 'id'
print(df); exit()
# Define the dynamic point layer
layer = pdk.Layer(
    "ScatterplotLayer",
    data=df,
    get_position=["lon", "lat"],
    get_color="[0, 150, 255, 200]",
    get_radius=80,
    pickable=True,
)

# Render/Update ONLY the layer data in the existing viewport
map_placeholder.pydeck_chart(
    pdk.Deck(
	    map_style="road",
        layers=[layer],
        tooltip={"text": "Bus ID: {id}"},
        initial_view_state=VIEW_STATE,
    )
)
time.sleep(REFRESH_INTERVAL_SECS)
st.rerun()
exit()





bus_details = get_bus_data(url, api_key)
if bus_details:
	for bus in bus_details:
		folium.CircleMarker(
			location=[bus["lat"], bus["lon"]],
			radius=6,
			color="blue",
			fill=True,
			fill_color="cyan",
			fill_opacity=0.7,
			popup=f"<b>Bus ID:</b> {bus['id']}<br><b>",
		).add_to(nyc_map)

	with map_placeholder.container():
	 	st_folium(nyc_map, width=1200, height=650, returned_objects=[])
       
            
# Hold thread state execution for 10 seconds before initiating the next network cycle
time.sleep(REFRESH_INTERVAL_SECS)
st.rerun()


