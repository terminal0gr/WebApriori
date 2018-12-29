<?php
include("config.php");
include("jwt_helper.php");
session_start(); 

$auth = false;

// Get data
if(isset($_POST['token']) &&
	isset($_POST['direction']) && 
	isset($_POST['origin_descr']) &&
	isset($_POST['destination_descr']) &&
	isset($_POST['departure_date'])) {
		$token = $_POST['token'];
		$SaveFilterName = $_POST['SaveFilterName'];
		$direction = $_POST['direction'];
		$nonstop = $_POST['nonstop'];
		$origin_descr = $_POST['origin_descr'];
		$destination_descr = $_POST['destination_descr'];

		$departure_date = $_POST['departure_date'];
		if ($departure_date != ""){
			$date = DateTime::createFromFormat('d/m/Y', $departure_date);
			$departure_date = $date->format('Y-m-d');
		}

		$return_date = $_POST['return_date'];
		if ($return_date != ""){
			$date = DateTime::createFromFormat('d/m/Y', $return_date);
			$return_date = $date->format('Y-m-d');
		}

		$FilterDate = date("Y-m-d H:i:s");
		
		try {
			// Get email
			$key=SERVERKEY.date("m.d.y");
			$email = JWT::decode($token, $key);
			$auth = true;
			} catch (\Exception $e) {  //hide $key on error
			echo 'error';
			}			
			
		if ($auth){
			// DB connection open	
			$con = new mysqli(HOST, USERNAME, PWD, DB);
			if (mysqli_connect_errno()) {
				printf("<BR>Fatal Error: %s\n", mysqli_connect_error());
				exit();
			}
			$sql="INSERT INTO filters(FilterEmail, FilterName, FilterDate, FilterOrigin, FilterDestination, FilterDDate, FilterRDate, FilterNonStop, FilterOneway)
					VALUES('$email','$SaveFilterName','$FilterDate','$origin_descr','$destination_descr','$departure_date','$return_date','$nonstop','$direction')";
			$result = mysqli_query($con,$sql);
			if($result){
				echo "Saved successfully";
			}
			else {
				echo "Filter name already exists";
			}
			mysqli_close($con);
		}
	}
else {
	echo "wrong data";
	}
	
	
session_destroy();
?>