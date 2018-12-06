<?php
   include_once 'config.php';

    header("Content-Type: application/json");
    header("Access-Control-Allow-Origin: *");
    //header("Content-Type: application/json; charset=UTF-8");

    $mysqli = new mysqli(HOST, USERNAME, PWD, DB);
	if (mysqli_connect_errno()) {
		printf("<BR>Connection error: %s\n", mysqli_connect_error());
        exit();
    } else {
        $query = "select city, country from airports where code = ?";
        $airline_code=$_REQUEST['code'];
        
        if ($stmt = $mysqli->prepare($query)) {
            $stmt->bind_param("s", $airline_code);
            $stmt->execute();
            $stmt->bind_result($city, $country);
            $stmt->fetch();
            $stmt->close();
            $airport = array('code' => $airline_code, 'city' => $city, 'country' => $country);
            print json_encode($airport);

        }
    
        $mysqli->close();
    }
    


    
?>
