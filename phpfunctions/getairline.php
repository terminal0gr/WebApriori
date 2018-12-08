<?php
   include_once '../config.php';

    header("Content-Type: application/json");
    header("Access-Control-Allow-Origin: *");

    $mysqli = new mysqli(HOST, USERNAME, PWD, DB);
	if (mysqli_connect_errno()) {
		printf("<br>Connection error: %s\n", mysqli_connect_error());
        exit();
    } else {
        $query = "select airline from airlines where iata = ?";
        $iata=$_REQUEST['iata'];
        
        if ($stmt = $mysqli->prepare($query)) {
            $stmt->bind_param("s", $iata);
            $stmt->execute();
            $stmt->bind_result($name);
            $stmt->fetch();
            $stmt->close();
            $airline = array('iata' => $iata, 'name' => $name);
            print json_encode($airline);

        }
    
        $mysqli->close();
    }
    
?>
