$(function() {

	// Get the form.
	var form = $('#ajax-SaveProfile');

	// Set up an event listener for the contact form.
	$(form).submit(function(e) {
		// Stop the browser from submitting the form.
		e.preventDefault();

		if (!checkForm()) return;

		if (!sessionStorage.getItem('token') || !sessionStorage.getItem('ProfileJSON')) {
			MyModal("Error","You must sign in!!!");
			setTimeout(function()
			{
				sessionStorage.clear();
				window.location.href='index.html';
			}, 3000);	
		}

		JsonProfile=JSON.parse(sessionStorage.getItem('ProfileJSON'));
		if (!JsonProfile) {
			MyModal("Error","You must sign in!!!");

			setTimeout(function()
			{
				sessionStorage.clear();
				window.location.href='index.html';
			}, 3000);	

		}

		// Serialize the form data.
		var formData = $(form).serialize();

		//Very important so to not lock in the profile state all the site
		sessionStorage.removeItem('ProfileJSON');

		// Submit the form using AJAX.
		$.ajax({
			type: 'POST',
			url: $(form).attr('action'),
			data: formData + '&token=' + sessionStorage.getItem('token') + '&oldemail=' + JsonProfile.email
		})
		.done(function(response) {

			res=JSON.parse(response);

			if (res.http_response_code==200) {
				sessionStorage.setItem('token', res.token);
				sessionStorage.setItem('apikey', res.apikey);
				sessionStorage.setItem('username', res.name);
				MyModal("Information","Profile settings saved successfully!");

				setTimeout(function()
				{
					location.reload();
				}, 3000);	
				 		
			} else {
				MyModal(res.title + '(' + res.http_response_code + ')',  res.message);
			}

		})
		.fail(function(data) {

			if (data.responseText) {
				MyModal("Flight Scanner",data.responseText);
			} else {
				MyModal("Flight Scanner",'Unknown error occured!');
			}
		});

	});

});


