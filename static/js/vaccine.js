console.log('Test Vaccine Site!!!!');
"use strict";


$('#vaccinesResults :button').on('click', (evt) => {
    let favorite = $(evt.target);
    evt.preventDefault();
  
    let data = {
         'vaccine_id': favorite.val()
      };
    $.post('/add_vaccine_site', data, (res) => {
        if (res['status']=='already_favorited') {
            $("#vaccine_info").html('Location exists.');
            
        } else {
            favorite.text("Location Saved"); 
        }
    
    });
  });

