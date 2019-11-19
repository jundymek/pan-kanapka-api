const button = document.querySelector(".addressButton");
const input = document.getElementById("autocomplete_search");
const lat = document.querySelector("#latit");
const lon = document.querySelector("#longit");

google.maps.event.addDomListener(window, "load");
button.addEventListener("click", firstInput);
const searchBox = new google.maps.places.SearchBox(input);
google.maps.event.addListener(searchBox, 'places_changed', firstInput)

const mymap = L.map("mapid").setView([52.237049, 21.017532], 13);

L.tileLayer("https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}", {
    attribution:
        'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
    maxZoom: 18,
    id: "mapbox.streets",
    accessToken: "pk.eyJ1IjoianVuZHltZWsiLCJhIjoiY2szMnZkMGpmMGs1OTNtcDlxa2lpbXdzOCJ9.WdtFFCpL3fWteMlL9liIjg"
}).addTo(mymap);


addMarkers()

function addMarkers() {
    for (let i = 0; i < places.length; i++) {
        console.log(places[i]);
        console.log(places[i].latitude, places[i].longitude)
        const marker = L.marker([places[i].latitude, places[i].longitude]).addTo(mymap);
        marker.bindPopup(`<b>${places[i].name}</b><br>I am a popup.`);
    }
}

function firstInput() {
    console.log('ddddddddddddddd')
    if (searchBox.getPlaces) {
        const [place] = searchBox.getPlaces();
        console.log(place)
        if (!place.geometry) return;
        // If the place has a geometry, then present it on a map.
        if (place.geometry.viewport) {
            console.log(place)
            const marker = L.marker([place.geometry["location"].lat(), place.geometry["location"].lng()]).addTo(mymap);
            lat.value = place.geometry["location"].lat();
            lon.value = place.geometry["location"].lng();
            marker.bindPopup(`<b>${place}</b><br>I am a popup.`).openPopup();
        } else {
            map.setCenter(place.geometry.location);
            map.setZoom(17);
        }
    }
}