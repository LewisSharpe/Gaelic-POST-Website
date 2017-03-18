% rebase("base.tpl", title="Informations about IP address", menu_type="infos", page_name="API Calls")

<script>
window.onload = function() {
    var map = L.map('map').setView([ {{lat}}, {{long}} ], 13);
    L.tileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
	attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="http://openstreetmap.org">OpenStreetMap</a>',
	maxZoom: 18
    }).addTo(map);


    var locate = L.marker([ {{lat}}, {{long}} ]).addTo(map);
    locate.bindPopup("{{ip}}");
    console.log("done");
};
</script>
<style>
#map {
    height: 300px;
}
</style>

<p> <strong>IP address:</strong> {{ip}} (<a href="{{base_url}}infos/api_calls/by_ip/{{ip}}">see all requests by this IP</a>)</p>
<p> <strong>Position:</strong> {{lat}} ; {{long}} </p>
<p> <strong>Country:</strong> {{country}} </p>
<p><em>Note: the location data may not be 100% accurate, depending on the country</em></p>

<div id="map"></div>

<link rel="stylesheet" href="http://cdn.leafletjs.com/leaflet-0.7.3/leaflet.css" />
<script src="http://cdn.leafletjs.com/leaflet-0.7.3/leaflet.js"></script>
