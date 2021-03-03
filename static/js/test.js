$('#vaccinesResults :button').on('click', (evt) => {
    let favorite = $(evt.target);
    evt.preventDefault();
  
    let data = {
         'vaccine_id': favorite.val()
      };
    $.post('/add_vaccine_site', data, (res) => {
        if (res['status']=='already_favorited') {
            $("#vaccine_info").html('Location exists.'); // does not show the message!!!!!!!!!
        } 
        else if (res['status']=='added') {
            favorite.text("Location Saved");
        }
        else {
            window.location.reload();
        }
    
    });
  });

