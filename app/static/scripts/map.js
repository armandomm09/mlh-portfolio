// Initialize map centered on your preferred location
var map = L.map('map').setView([0, 0], 1.5);

// Add OpenStreetMap tiles
L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);



const armandoPlaces = [
  { name: "Puebla, México", coords: [19.033333, -98.183334] },
  { name: "Heidelberg, Alemania", coords: [49.409360, 8.694723] },
  { name: "Berlín, Alemania", coords: [52.520008, 13.404954] },
  { name: "California, USA", coords: [36.778259, -119.417931] },
  { name: "Miami, USA", coords: [25.761681, -80.191788] },
  { name: "Seattle, USA", coords: [47.608013, -122.335167] },
  { name: "Bath, Inglaterra", coords: [51.380001, -2.360000] },
  { name: "Londres, Inglaterra", coords: [51.509865, -0.118092] },
  { name: "Argentina (Buenos Aires)", coords: [-34.603722, -58.381592] }
];



armandoPlaces.forEach(place => {
    var marker  = L.marker(place.coords)
     .addTo(map)
     .bindPopup(`<b>${place.name}</b>`)
     marker._icon.classList.add("huechange");
});

