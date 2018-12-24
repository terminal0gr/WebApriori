<?php
   include_once 'config.php';
   include_once 'functions.php';
   include_once 'jwt_helper.php';

    header("Content-Type: application/json");
    header("Access-Control-Allow-Origin: *");

    $mysqli = new mysqli(HOST, USERNAME, PWD, DB);
	if (mysqli_connect_errno()) {
        http_response_code(500);
		printf("<br>Connection error: %s\n", mysqli_connect_error());
        exit();
    } else {

        $iata=$_REQUEST['iata'];
        $token = $_REQUEST['token'];
        if(!$token) {
            http_response_code(403);
            echo "Flight Scanner. Access denied!!! Error(Retrieving airlines 1)";
            exit();
        }

        $key=SERVERKEY.date("m.d.y");

        try {
            $email=JWT::decode($token, $key);
        } catch (Exception $e) {
            http_response_code(403);
            echo "Flight Scanner. Access denied!!! Error(Retrieving airlines 1.1)";
            exit();
        }

        if(!$email) {
            http_response_code(403);
            echo "Flight Scanner. Access denied!!! Error(Retrieving airlines 2)";
            exit();
        }

        $email = mysqli_real_escape_string($mysqli, $email);
        $query ="SELECT * FROM usertable WHERE email='$email'";
        $result = mysqli_query($mysqli,$query);
        $num=mysqli_num_rows($result);
        if($num!==1){
            http_response_code(403);
            echo "Flight Scanner. Access denied!!! Error(Retrieving airlines 3)";
            exit();
        }
                
        $query = "select airline from airlines where iata = ?";
        
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
