% rebase("base.tpl", title="API Calls on a map", menu_type="infos", page_name="API Calls")

<script>
window.onload = function() {
    var map = L.map('map').setView([0, 0], 2);
    L.tileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
	attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="http://openstreetmap.org">OpenStreetMap</a>',
	maxZoom: 18
    }).addTo(map);

    function addMarkerOnMap(lat, long, ip, count) {
	L.marker([ parseInt(lat), parseInt(long) ])
	    .bindPopup("<a href={{base_url}}infos/ip/" + ip + ">" + ip + "</a><br>" + count + " use" + ((count > 1) ? "s" : ""))
	    .addTo(map);
    }

    % for ip_and_count in ips:
	      % ip, count = ip_and_count
    % ip_safe = ip.replace('.', '')
	var req_{{ip_safe}} = new XMLHttpRequest();
    req_{{ip_safe}}.open("GET", "{{base_url}}infos/get_location_from_ip/{{ip}}", true);
    req_{{ip_safe}}.onreadystatechange = function(evt) {
	if (req_{{ip_safe}}.readyState == 4) {
	    if (req_{{ip_safe}}.status == 200) {
		var result = JSON.parse(req_{{ip_safe}}.responseText);
		if (!result.error)
		    addMarkerOnMap(result['latitude'], result['longitude'], result['ip'], {{count}});
		else
		    console.log("Error : " + result.error);
	    }
	}
    };
    req_{{ip_safe}}.send(null);

    % end
};
</script>
<style>
#map {
    height: 600px;
}
</style>

<div id="content">
    <div id="map"></div>
</div>

<link rel="stylesheet" href="http://cdn.leafletjs.com/leaflet-0.7.3/leaflet.css" />
<script src="http://cdn.leafletjs.com/leaflet-0.7.3/leaflet.js"></script>
