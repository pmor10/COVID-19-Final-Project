"use strict";

$('#logInForm').on('submit', (evt) => {
    evt.preventDefault();

    let password = $('#logInPassword').val();
    let username = $('#logInUsername').val();

    $.post('/login', {'username': username, 'password': password}, (result) => {
        if (result.username_found == false) { // username does not exist
            $('#logInErrorMessage').html("Error: Username not recognized.")
            $('#logInErrorMessage').fadeIn(400, () => {
                setTimeout(() => {$('#logInErrorMessage').fadeOut(400,)}, 5000);
            });
        }
        else { // username exists
            if (result.valid_login == false) { // username and password do not match
                $('#logInErrorMessage').html("Error: Username and password do not match")
                $('#logInErrorMessage').fadeIn(400, () => {
                    setTimeout(() => {$('#logInErrorMessage').fadeOut(400,)}, 5000);
                });
            }
            else {
                // login is valid, user is logged in in backend, user go to homepage
                window.location.href = '/';
            }
        }
    });
    
});