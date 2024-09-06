<?php

    if (!isset($_POST['a'])) {
        http_response_code(400);
        $JsonReq = array('title' => 'Error', 'message' => 'a not given');
        print json_encode($JsonReq);
        exit();
    }
    if (!isset($_POST['b'])) {
        http_response_code(400);
        $JsonReq = array('title' => 'Error', 'message' => 'b not given');
        print json_encode($JsonReq);
        exit();
    }
    if (!isset($_POST['callType'])) {
        http_response_code(400);
        $JsonReq = array('title' => 'Error', 'message' => 'callType not given');
        print json_encode($JsonReq);
        exit();
    }

    $a=$_POST['a'];
    $b=$_POST['b'];
    // $a="aBC";
    // $b="DEf";

    if (isset($_POST['callType']) && $_POST['callType'] == 0) {
        $Call = "http://localhost:8081/run-script";
    } else {
        $Call = "http://localhost:8081/run-script1";
    }

    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, $Call);
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