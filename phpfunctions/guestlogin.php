<?php
	include("config.php");
	session_start(); 
    
	if ($_SERVER["REQUEST_METHOD"] == "POST") {

		http_response_code(200);
        $JsonReq = array('http_response_code' => 200, 'token' => '0', 'name' => 'guest', 'message' => 'success');
        print json_encode($JsonReq);

	} else {
		// Not a POST request, set a 403 (forbidden) response code.
		http_response_code(403);
		echo "There was a problem with your submission, please try again.";
	}
?>

