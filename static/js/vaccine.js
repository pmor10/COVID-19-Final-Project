"use strict";


$('#vaccinesResults :button').on('click', (evt) => {

    evt.preventDefault();
    let favorite = $(evt.target);

  
    let data = {
         'vaccine_id': favorite.val()
      };
    $.post('/add_vaccine_site', data, (res) => {

        if (res['status']==='already_favorited') {
            
            favorite.text("Location exists");
            //alert("Location already saved!");
        } else if (res['status']==='added') {
            favorite.text("Location Saved");
            //alert("Location saved!");
        }
       // window.location.reload(true);
    });
  });


  let map;

  function initMap() {
    map = new google.maps.Map(document.getElementById("map"), {
      zoom: 5,
      center: new google.maps.LatLng(34.081292,  -117.996576),
      mapTypeId: "terrain",
    });
    // Create a <script> tag and set the USGS URL as the source.
    const script = document.createElement("script");
    // This example uses a local copy of the GeoJSON stored at
    // http://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/2.5_week.geojsonp
    
    //script.src = {"content": {"Latitude": 34.081292, "Longitude": -117.996576}};


     //document.getElementsByTagName("head")[0].appendChild(script);
     callback({"content": [{"Latitude": 34.081292, "Longitude": -117.996576}]});
  }
  
  // Loop through the results array and place a marker for each
  // set of coordinates.
  const callback = function (results) {
    for (let i = 0; i < results.content.length; i++) {
      
      const lon = results.content[i].Latitude;
      const lat = results.content[i].Longitude;
      const latLng = new google.maps.LatLng(lat, lon);
      new google.maps.Marker({
        position: latLng,
        map: map,
      });
    }

  };

  
  
  