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
			// Make sure that the formMessages div has the 'success' class.
			$(formMessages).removeClass('error');
			$(formMessages).addClass('success');

			res=JSON.parse(response);

			if (res.http_response_code==200) {
				sessionStorage.setItem('token', res.token);
				sessionStorage.setItem('username', res.name);
				window.location.href='index.html';
			} else {
				$(formMessages).text('An error occured.<br>' + res.http_response_code + ' ' + res.message)

			}

		})
		.fail(function(data) {
			// Make sure that the formMessages div has the 'error' class.
			$(formMessages).removeClass('success');
			$(formMessages).addClass('error');

			if (data.responseText) {
				$(formMessages).text(data.responseText);
			} else {
				$(formMessages).text('An error occured.');
			}
		});

	});

});


