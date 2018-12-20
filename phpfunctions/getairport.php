<?php
   include_once 'config.php';
   include_once 'functions.php';

    header("Content-Type: application/json");
    header("Access-Control-Allow-Origin: *");


    
    $mysqli = new mysqli(HOST, USERNAME, PWD, DB);
	if (mysqli_connect_errno()) {
        $airport = array('code' => $_REQUEST['code'], 'city' => '', 'country' => '', 'Message' => 'Connection error:'.mysqli_connect_error());
        print json_encode($airport);
        exit();
    } else {
        $query = "select city, country from airports where code = ?";
        $iata_code=$_REQUEST['code'];
        
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
