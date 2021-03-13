"use strict";

$(document).on('click', '#add_button',  (evt) => {

    let favorites = []; 

    $('.get_value').each(function() {
        if ($(this).is(":checked")) {
            favorites.push($(this).val());
        } else {
            window.location.reload(true);
        }
    });
})


