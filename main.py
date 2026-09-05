#!/Users/fabiandeleon/.pyenv/shims/python
import os
import uvicorn
from main_functions import *
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

api_key = get_api_key(f'{os.getcwd()}/../api_keys/mta_api')
urlvehicle=f'https://gtfsrt.prod.obanyc.com/vehiclePositions?key={api_key}'
urldelay=f'https://gtfsrt.prod.obanyc.com/tripUpdates?key={api_key}'

class MapBounds(BaseModel):
    south: float
    west: float
    north: float
    east: float

app = FastAPI(title="Live Bus GeoJSON API")
app.state.map_bounds = None
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/images", StaticFiles(directory="images"), name="images")

@app.get("/")
def read_index():
    return FileResponse("static/map.html")

# Endpoint to receive and print bounds
@app.post("/api/print-bounds")
async def receive_bounds(bounds: MapBounds):
    app.state.map_bounds = bounds
    print("\n================ MAP BOUNDS RECEIVED ================")
    print(f"Bounds {bounds}")
    print("=====================================================\n")
    
    return {"status": "success", "bounds": bounds.model_dump()}

@app.get("/api/buses.geojson")
def get_buses_geojson():
    bus_list = merge_bus_data(urlvehicle, urldelay, app.state.map_bounds)
    print(bus_list)
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
                "id": bus["id"],
                "delay": bus["delay"]
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