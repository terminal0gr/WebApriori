$(function() {

	// Get the form.
	var form = $('#ajax-contact');

	// Get the messages div.
	var formMessages = $('#form-messages');

	// Set up an event listener for the contact form.
	$(form).submit(function(e) {
		// Stop the browser from submitting the form.
		e.preventDefault();

		// Serialize the form data.
		var formData = $(form).serialize();

		// Submit the form using AJAX.
		$.ajax({
			type: 'POST',
			url: $(form).attr('action'),
			data: formData
		})
		.done(function(response) {

			res=JSON.parse(response);

			if (res.http_response_code==200) {
				sessionStorage.setItem('token', res.token);
				sessionStorage.setItem('apikey', res.apikey);
				sessionStorage.setItem('username', res.name);
				window.location.href='index.html';
			} else {
				alert('An error occured.<br>' + res.http_response_code + ' ' + res.message);
			}

		})
		.fail(function(data) {

			if (data.responseText) {
				alert(data.responseText);
			} else {
				alert('An error occured.');
			}
		});

	});

});


