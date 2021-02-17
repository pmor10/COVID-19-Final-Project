// Show Testing Location Address
function showTestingLocation(evt) {
    evt.preventDefault();

    let url = "localhost/5000/testing";
    let formData = {"zipcode": $("#zipcode-field").val()};

    $.get(url, formData, function (results) {
        $("#location-info").html(results.????);
    });
}

$("#testing-location-form").on('submit', showTestingLocation);







// Add fav. Locations

// const addSavedLocation = (address) => {

// }