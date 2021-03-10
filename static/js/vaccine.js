"use strict";

$('#vaccineSearchForm').on('submit', (evt) => {
  
  evt.preventDefault();
  
  let zipcode = $('#zip_code ').val();
  let data = {'zip_code': zipcode};
  
  $('.vac-show-info').removeClass('invisible');
  $('.vac-show-info').addClass('visible');

  $.get('/get_geojson_by_zip', data, (res) => {
    // Draws the google map markers    
    console.log(res);
    callback(res);
  })
  
 
  $.get('/get_zipcode_data', data, (res1) => {
    // stores the data in locations 
    const locations = res1    
    $( "#vaccine_content" ).empty();
    let table = ''; 

    for (let i in locations) {
      
      let row = '<ul class="location-details">' 
      row += '<li class="facility-name">' + locations[i]['name'] + '</li>';
      row += '<li class="bi bi-geo-alt-fill">' + locations[i]['address'] + '</li>';
      row += '<li><i class="bi bi-calendar2-check-fill"></i> Appointment Required</li>';
      row += '<li><button id="add_button" type="button" class="save_vaccine_location btn btn-button btn-width-auto" value=' + i + '>Save Location</button></li>';
      row += '</ul>'
      table += row 
      }
      $('#vaccine_content').append(table);
      }
      ) 
  
});

$(document).on('click', '#add_button', (evt) => {

  let favorite = $(evt.target);

  let data =  {
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
    const coords = {lat:37.265443,  lng:-121.941761};
    // console.log(coords); 
    map = new google.maps.Map(document.getElementById("map"), {
      zoom: 12,
      center: coords,

    });
    //  This applies the overlay to the map for the marker
    // const marker = new google.maps.Marker({position: coords,
    //                                         map: map, 
    //                                       });
    
                                        }

  const callback = function (results) {


    for (let i = 0; i < results.features.length; i++) {

        const coords = results.features[i].geometry.coordinates;
        const latLng = new google.maps.LatLng(coords[1], coords[0]);

        const contentString =
              '<div id="content">' +
              '<div id="siteNotice">' +
              "</div>" +
              '<h5 id="firstHeading" class="firstHeading">'+results.features[i].properties.name+'</h5>' +
              '<div id="bodyContent">' +
              '<p>' + results.features[i].properties.address + '</p>' +
              "</div>" +
              "</div>";

        const infowindow = new google.maps.InfoWindow({
          content: contentString,
        });

        let marker = new google.maps.Marker({
          position: latLng,
          map: map,

        });
      
        map.setCenter(latLng);

        marker.addListener("click", () => {
          infowindow.open(map, marker);
          });
  }
};  