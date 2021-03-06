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
            // alert("Location already saved!")
        } else if (res['status']==='added') {
            favorite.text("Location Saved");
        }
        window.location.reload(true);
    });
  });


// Initialize and add the map
function initMap() {
  // The location of Uluru
  const uluru = { lat: 36.778259, lng: -119.417931 };
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