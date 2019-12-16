$(function() {

	// Get the form.
	var form = $('#ajax-contact');

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
		.done(function(response, textStatus, jqXHR) {
			if (isJSON(response)) {
				res=JSON.parse(response);

				if (jqXHR.status==200) {
					sessionStorage.setItem('token', res.token);
					sessionStorage.setItem('username', res.name);
					sessionStorage.setItem('administrator', res.administrator);		
					sessionStorage.setItem('grandPublicDatasets', res.grandPublicDatasets);
					window.location.href='search.html';
				} else {
					MyModal("An error occured",res.message);
				}
			} else {
				MyModal("Information", response)
			}

		})
		.fail(function( jqXHR, textStatus, thrownError ) {
			if (jqXHR.responseText) {
				if (isJSON(jqXHR.responseText)) {
					res=JSON.parse(jqXHR.responseText);
					MyModal(res.title, res.message);
				}
				else alert(jqXHR.responseText);

			} else {
				MyModal("WebApriori",'Unknown error occured!');
			}
		});

	});

});


