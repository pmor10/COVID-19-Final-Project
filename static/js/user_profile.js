"use strict";

$('#btnRemove').on('click', (evt) => {
    evt.preventDefault();
    let favorite = $(evt.target);
    console.log(favorite)
    let data = {
         'vaccine_id': favorite.val()
      };
    $.post('/delete_vaccine', data, (res) => {
       window.location.reload(true);
    });
  });


