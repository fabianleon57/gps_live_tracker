#!/Users/fabiandeleon/.pyenv/shims/python
import uvicorn
from main_functions import *
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

api_key='2fcc6aee-7345-4499-aee3-bdcd1087bc00'
url=f'https://gtfsrt.prod.obanyc.com/vehiclePositions?key={api_key}'


app = FastAPI(title="Live Bus GeoJSON API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def read_index():
    return FileResponse("static/map.html")

@app.get("/api/buses.geojson")
def get_buses_geojson():
    bus_list = merge_bus_data(url,api_key)
    features = []
    for bus in bus_list:
        feature = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                # Note: GeoJSON standards strictly use [Longitude, Latitude] order
                "coordinates": [bus["lon"], bus["lat"]]
            },
            "properties": {
                "id": bus["id"], "delay": bus["delay"]
            }
        }
        features.append(feature)
        
    # Return standard GeoJSON FeatureCollection
    return {
        "type": "FeatureCollection",
        "features": features
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)