<?php
   include_once 'config.php';

    //header("Content-Type: application/json");
    header("Access-Control-Allow-Origin: *");
    header("Content-Type: application/json; charset=UTF-8");

	$mysqli = new mysqli(HOST, USERNAME, PWD, DB);
	if (mysqli_connect_errno()) {
		printf("<BR>Connection error: %s\n", mysqli_connect_error());
        exit();
    } else {
        $query = "select city, country from airports where code = ?";
        $airline_code=$_REQUEST['code'];
        
        printf($airline_code);
        
        if ($stmt = $mysqli->prepare($query)) {
            $stmt->bind_param("s", $airline_code);
            $stmt->execute();
            $stmt->bind_result($city, $country);
            $stmt->fetch();
            $stmt->close();
            
            printf('just before');
            $airport = $city.",<br>".$country;
            printf($airport);
            printf('just after');
    
            // $stmt->bind_param("s", $airline_code);
            // $stmt->execute();
            // $stmt->bind_result($airline);
            // $rows = array();
            // while($r = mysqli_fetch_assoc($stmt)) {
            //     $rows[] = $r;
            // }
    
            http_response_code(200);
    
            return $airport;
            //print json_encode($rows);
        }
    
        $mysqli->close();
    }
    


    
?>
