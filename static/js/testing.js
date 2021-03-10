"use strict";

// create map
let map;

function initMap() {
  const coords = {lat:37.265443,  lng:-121.941761};
  // console.log(coords); 
  map = new google.maps.Map(document.getElementById("map"), {
    zoom: 12,
    center: coords,

  });
};


$('#testingSearchForm').on('submit', (evt) => {
  
  evt.preventDefault();
  
  let zipcode = $('#zip_code').val();
  let data = {'zip_code': zipcode};
  
  $('.testing-show-info').removeClass('invisible');
  $('.testing-show-info').addClass('visible');

  $.get('/get_testing_locations_by_zip', data, (res1) => {
    // stores the data in locations 
    const locations = res1    
    $( "#testing_content" ).empty();
    let table = ''; 

    for (let i in locations) {
      let name = locations[i]['alternate_name']; 
      let addr = locations[i]['address'] + ' ' + locations[i]['city'] + ' ' + locations[i]['state_province'] + ' ' + locations[i]['zip_code']; 

      let row = '<ul class="location-details">';
      row += '<li class="facility-name">' + name + '</li>';
      row += '<li class="bi bi-geo-alt-fill">' + addr + '</li>';
      row += '<li><i class="bi bi-calendar2-check-fill"></i> Appointment Required</li>';
      row += '<li class="button-site"><button id="add_button" type="button" class="save_testing_location btn btn-button btn-width-auto" value=' + i + '>Save Location</button></li>';
      row += '</ul>';
      table += row ;
      
      
      geolocator(addr, map, name);
      
      }
      
      // map.setCenter(addr);

      // marker.addListener("click", () => {
      //   infowindow.open(map, marker);
      //   });

      $("#testing_content").append(table);

      }
      ) 
    
  });



$(document).on('click', '#add_button', (evt) => {

    let favorite = $(evt.target);  
  
    let data =  {
                  'test_id': favorite.val()
                };
    
    $.post('/add_testing_site', data, (res) => {
      
      console.log(res);
      if (res['status']==='already_favorited') {
            favorite.text("Location exists");
            
        } else if (res['status']==='added') {
            favorite.text("Location Saved"); 
        } 
    });
  });

  


// determine where to center map
function geolocator(address, themap, name) {
  let location = new google.maps.Geocoder();

  location.geocode(
                    {'address': address}, 
                    function (results, status) 
                            {
                              // geocodes successfully
                              let pos = results[0].geometry.location;
                              themap.setCenter(pos);
                              
                              if (status === google.maps.GeocoderStatus.OK) {
                                let marker = new google.maps.Marker({
                                  position: pos,
                                  map: map,
                                });
                                
                                let infoWindow = new google.maps.InfoWindow({
                                  width: 150
                              });
                              let html = (
                                '<div>' +
                                '<h5>' + name + '</h5>' +
                                '<p>' + address + '</p>' +
                                '</div>'
                            );
                                marker.addListener("click", () => {
                                  infoWindow.close();
                                  infoWindow.setContent(html);
                                  infoWindow.open(themap, marker);
                                  
                                  });
                                 
                              } 
                              
                            } 

                    )
    
};


