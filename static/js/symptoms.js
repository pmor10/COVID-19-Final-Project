"use strict";
// check if a symptom is checked
$(document).on('click', '#add_button',  (evt) => {
    evt.preventDefault();
    let favorites = []; 
    
    $('.get_value').each(function() {

        if ($(this).is(":checked")) {
            favorites.push($(this).val());
        } 

    });
    // make a json of the array
    let data = JSON.stringify({'data':favorites}); 

    $.post('/add_symptoms', data, (res) => {

        let symptoms = "";

        if (res.added_symptoms.length !=0) {

            for (var i = 0; i < res.added_symptoms.length; i++) {
            
                symptoms = symptoms + res.added_symptoms[i] + ', ';
        
            }
            symptoms += "added to your profile"
        } else {
             symptoms = "Symptoms already added to your profile";
        }

        $('<p class="display-message alert alert-primary">' + symptoms + '</p>').insertAfter('.site-search').delay(3000).fadeOut();
        
        }
    );

   



})


