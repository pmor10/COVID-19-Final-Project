"use strict";

$(document).ready(function() {
    $('#add_button').click(function() {
        let favorites = []; 
        $('.get_value').each(function() {
            if ($(this).is(":checked")) {
                favorites.push($(this).val());
            }
        });
        
        $.ajax({
            type: "POST",
            contentType: 'application/json',
            dataType :"json",
            url: "/add_symptoms",
            data: JSON.stringify(favorites),
            cache: false,
            success: function(data) {
                $("#result").html(data);
            }
        });
    });
});


