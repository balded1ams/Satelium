const R = 6378;

const map = L.map('map').setView([0, 0], 2);

var markers = {}

function initMarkers() {
    for (const sat of Object.values(markers)) {
        map.removeLayer(sat.marker)
        map.removeLayer(sat.footprint)
    }
    markers = {}

    var trackedSats = JSON.parse(localStorage.getItem("trackedSats"))
    if (trackedSats === null) return
    for (const sat of trackedSats) {
        const icon = L.divIcon({
          className: '',
          html: `<div style="text-align: center;">${sat}</div>`,
          iconSize: [100, 30],
          iconAnchor: [50, 15]
        });
        markers[sat] = {
            marker: L.marker([0, 0], { icon: icon }),
            footprint: L.circle([0, 0], 100000)
        };
        markers[sat].marker.addTo(map)
        markers[sat].footprint.addTo(map)
    }
}

L.tileLayer(
    'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
    {noWrap: true}
).addTo(map);


setInterval(() => {
    for (const [id, sat] of Object.entries(markers)) {
        fetch(`/api/position?norad_id=${id}`)
        .then(data => data.json())
        .then(data => {
            sat.marker.setLatLng([data.lat, data.lon]);
            sat.footprint.setLatLng([data.lat, data.lon]);
            sat.footprint.setRadius(R*Math.acos(R/(R+data.alt))*1000)
        });
    }
}, 1000);

initMarkers()