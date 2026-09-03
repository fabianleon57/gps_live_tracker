// 1. Initialize Map Canvas
const map = L.map('map').setView([40.7128, -74.0060], 12);

// Standard OpenStreetMap tiles (Reliable fallback tile server)
L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

// Ensure Leaflet recalculates viewport bounds on load
setTimeout(() => {
    map.invalidateSize();
}, 100);

// Create a persistent layer group for markers
const busLayer = L.layerGroup().addTo(map);
var busIcon = L.Icon.extend({
    options: {
        iconSize:     [10, 10],
        iconAnchor:   [5, 5],
        popupAnchor:  [-3, -3]
    }
});
var greenBus = new busIcon({iconUrl: 'images/greenbus.png'}),
    redBus = new busIcon({iconUrl: 'images/redbus.png'});

// 2. Fetch GeoJSON from FastAPI and update vector points
async function updateMap() {
    try {
        const response = await fetch('/api/buses.geojson');
        const data = await response.json();

        busLayer.clearLayers();

        L.geoJSON(data, {
            pointToLayer: function (feature, latlng) {
                var isDelayed = feature.properties.delay > 0;
                const props = feature.properties;
                return L.marker(latlng, 
                                {icon: isDelayed ? redBus : greenBus}
                                ).bindPopup(`<b>Bus ID:</b> ${props.id || 'N/A'}
                                            <br><b>Delay:</b> ${ isDelayed ? props.delay : "On Time" || 'N/A'}`);
            },
            // onEachFeature: function (feature, layer) {
            //     var isDelayed = feature.properties.delay > 0; 
            //     if (feature.properties) {
            //         const props = feature.properties;
            //         layer.bindPopup(`<b>Bus ID:</b> ${props.id || 'N/A'}
            //                         <b>Delay:</b> ${ isDelayed ? props.delay : "On Time" || 'N/A'}`);
            //     }
            // }
        }).addTo(busLayer);

    } catch (error) {
        console.error("Error updating map points:", error);
    }
}

updateMap();
setInterval(updateMap, 30000); 