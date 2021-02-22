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

