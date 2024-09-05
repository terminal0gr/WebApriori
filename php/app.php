<?php

    $a="Lumen";
    $b="Arben";

    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, "http://localhost:8081/run-script");
    curl_setopt($ch, CURLOPT_POST, 1);
    curl_setopt($ch, CURLOPT_POSTFIELDS, http_build_query(array('a' => $a, 'b' => $b)));  // Passing data
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    $response = curl_exec($ch);
    curl_close($ch);

    //echo $response;

    http_response_code(202);
    $jsonReq = array('title' => "no excuse" , 'message' => $response);
    print json_encode($jsonReq);
    exit();   

?>