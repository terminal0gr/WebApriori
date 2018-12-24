<?php
   include_once 'config.php';
   include_once 'functions.php';
   include_once 'jwt_helper.php';

    header("Content-Type: application/json");
    header("Access-Control-Allow-Origin: *");
    
    $mysqli = new mysqli(HOST, USERNAME, PWD, DB);
	if (mysqli_connect_errno()) {
        $airport = array('code' => $_REQUEST['code'], 'city' => '', 'country' => '', 'Message' => 'Connection error:'.mysqli_connect_error());
        print json_encode($airport);
        exit();
    } else {

        $iata_code=$_REQUEST['code'];
        $token = $_REQUEST['token'];
        if(!$token) {
            http_response_code(403);
            echo "Flight Scanner. Access denied!!! Error(Retrieving airports 1)";
            exit();
        }

        $key=SERVERKEY.date("m.d.y");

        try {
            $email=JWT::decode($token, $key);
        } catch (Exception $e) {
            http_response_code(403);
            echo "Flight Scanner. Access denied!!! Error(Retrieving airports 1.1)";
            exit();
        }
        
        if(!$email) {
            http_response_code(403);
            echo "Flight Scanner. Access denied!!! Error(Retrieving airports 2)";
            exit();
        }

        $email = mysqli_real_escape_string($mysqli, $email);
        $query ="SELECT * FROM usertable WHERE email='$email'";
        $result = mysqli_query($mysqli,$query);
        $num=mysqli_num_rows($result);
        if($num!==1){
            http_response_code(403);
            echo "Flight Scanner. Access denied!!! Error(Retrieving airports 3)";
            exit();
        }

        $query = "select city, country from airports where code = ?";
        
        if ($stmt = $mysqli->prepare($query)) {
            $stmt->bind_param("s", $iata_code);
            $stmt->execute();
            $stmt->bind_result($city, $country);
            $stmt->fetch();
            if ($city) {
                $airport = array('code' => $_REQUEST['code'], 'city' => $city, 'country' => $country, 'Message' => 'Airport found in Database');
                print json_encode($airport);
                exit();
            } else {
                ini_set("allow_url_fopen", 1); 

                //https://api.sandbox.amadeus.com/v1.2/location/SMI?apikey=TZXCihIgRAkexLGxXtsVmfuyJpwHlp82
                $request = "https://api.sandbox.amadeus.com/v1.2/location/".$iata_code."?apikey=".apikey;

                 $response = @file_get_contents($request);
                 $code = getHttpCode($http_response_header);

                if($code <> 200) {
                    $airport = array('code' => $_REQUEST['code'], 'city' => '', 'country' => '', 'Message' => 'Airport not found');
                    print json_encode($airport);
                    exit();
                }

                $jsonobj = json_decode($response);

                if (!$jsonobj->city) {
                    $airport = array('code' => $_REQUEST['code'], 'city' => '', 'country' => '', 'Message' => 'Airport not found');
                    print json_encode($airport);
                    exit();
                }

                $query = "insert into airports (code, city, country)
                          values (?,?,?)";
                if ($stmt = $mysqli->prepare($query)) {
                    $stmt->bind_param("sss", $A, $B, $C);
                    $A=$_REQUEST['code'];
                    $B=$jsonobj->city->name;
                    $C=$jsonobj->city->country;
                    $stmt->execute();
                }
                
                $airport = array('code' => $_REQUEST['code'], 'city' => $jsonobj->city->name, 'country' => $jsonobj->city->country, 'Message' => 'Airport retrieved from API');
                print json_encode($airport);
                exit();
            }
        }
    }
    
?>
