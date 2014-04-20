function drawRoute(fromLat, fromLng, toLat, toLng) {
    var directionsService = new google.maps.DirectionsService();
    var directionsDisplay = new google.maps.DirectionsRenderer();

    var bounds = new google.maps.LatLngBounds();
    var from = new google.maps.LatLng(fromLat, fromLng);
    var to = new google.maps.LatLng(toLat, toLng);

    var mapOptions = {
        mapTypeId: google.maps.MapTypeId.ROADMAP
    };

    map = new google.maps.Map(document.getElementById("map_canvas"), mapOptions);

    directionsDisplay.setMap(map);
     
    fromMarker = new google.maps.Marker({
        position: from,
        title: 'Start'
    });
    bounds.extend(fromMarker.position);

    toMarker = new google.maps.Marker({
        position: to,
        title: 'End'
    });
    bounds.extend(toMarker.position);

    var request = {
        origin: from,
        destination: to,
        travelMode: google.maps.TravelMode.DRIVING
    }
    directionsService.route(request, function(response, status) {
        if (status == google.maps.DirectionsStatus.OK) {
            directionsDisplay.setDirections(response);
        }
    });

    map.fitBounds(bounds);
}

function drawMarker(lat, lng) {

    var point = new google.maps.LatLng(lat, lng);

    var mapOptions = {
        mapTypeId: google.maps.MapTypeId.ROADMAP,
        center: point,
        zoom: 15
    };

    map = new google.maps.Map(document.getElementById("map_canvas"), mapOptions);
    
    marker = new google.maps.Marker({
        position: point
    });

    marker.setMap(map);
}