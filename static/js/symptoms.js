console.log("TESTING SYMPTOMS1");
"use strict";

$(document).ready(function() {
    $('#add_button').click(function() {
        console.log('Button clicked.');
        let favorites = []; 
        $('.get_value').each(function() {
            if ($(this).is(":checked")) {
                console.log($(this).val());
                favorites.push($(this).val());
                console.log(favorites);
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







// let favorites = new Set();
// $('form input:checkbox').on('click', (evt) => {
//     evt.preventDefault();
//     favorite =  $(evt.target);
//     favorites.add(favorite.val());
//     console.log(favorites);
    
    
//     data = {'symptom_id':favorites};
    
//     $.post('/add_symptoms', data, (res) => {
//         alert(res);
    
//     });
//   });

