"use strict";


$('#removeVaccine :button').on('click', (evt) => {
    let favorite = $(evt.target);
    evt.preventDefault();
  
    let data = {
         'vaccine_id': favorite.val()
      };
    $.post('/delete_vaccine', data, (res) => {
            $("#btnRemove").remove();
            window.location.reload();
    
    });
  });


function removeVaccine() {
    let elem = document.getElementById('removeVaccine');
    elem.parentNode.removeChild(elem);
    return false;
}