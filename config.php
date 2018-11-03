<?php
	//$link = mysqli_connect("127.0.0.1", "flightsuser", "flightsuser", "flightsdata");
	$mysqli = new mysqli("127.0.0.1", "flightsuser", "flightsuser", "flightsdata");
	/* check connection */
	if (mysqli_connect_errno()) {
		printf("Connect failed: %s\n", mysqli_connect_error());
		exit();
	}
?>