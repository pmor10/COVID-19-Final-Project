"use strict";

$("#testingsResults :button").on('click', (evt) => {

    let favorite = $(evt.target);
    evt.preventDefault();
  
    let data = {
         'test_id': favorite.val()
      };
    
    $.post('/add_testing_site', data, (res) => {
        if (res['status']=='already_favorited') {
            $("#test_info").html('Location exists.');
            
        } else {
            favorite.text("Location Saved"); 
        }
    
    });
  });



// Initialize and add the map
function initMap() {
    // The location of Uluru
    const uluru = { lat: -25.344, lng: 131.036 };
    // The map, centered at Uluru
    const map = new google.maps.Map(document.getElementById("map"), {
      zoom: 4,
      center: uluru,
    });
    // The marker, positioned at Uluru
    const marker = new google.maps.Marker({
      position: uluru,
      map: map,
    });
  }
