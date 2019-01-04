<?php
	include("config.php");
	include("jwt_helper.php");
	session_start(); 
	
	$auth = false;

	$con1 = new mysqli(HOST, USERNAME, PWD, DB);
	
	/* check connection */
	if ($con1->connect_error) {
		die("Connection Error" . $con1->connect_error);
	}
    
	if ($_SERVER["REQUEST_METHOD"] == "POST") {

        if (!isset($_POST['token'])) {
			echo "wrong request!!!";
			exit();
		}

		try {
			// Get email
			$key=SERVERKEY.date("m.d.y");
			$email = JWT::decode($_POST['token'], $key);
			$auth = true;
		}
		catch (Exception $e) {  //hide $key on error
			echo 'Authentication error!!!';
			exit();
		}			
			
		if (!$auth) {
			echo 'Authentication error!!!';
			exit();
		}

		$query ="SELECT * FROM usertable WHERE email='$email'";
		$result = mysqli_query($con1,$query);

		if (mysqli_num_rows($result) == 0) {
			echo 'User not found!!!';
			exit();			
		}

		$group_arr = mysqli_fetch_assoc($result); 
		$result->close();
		echo json_encode($group_arr);
	}
?>	