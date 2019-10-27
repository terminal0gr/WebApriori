<?php
    include("config.php");
	include("jwt_helper.php");
    session_start(); 

    $auth = false;

    if (!isset($_POST['token'])) {
        http_response_code(400);
        $JsonReq = array('http_response_code' => 400, 'title' => 'Error', 'message' => 'You are not signed in!!! Please sign in/up');
        print json_encode($JsonReq);
        exit();
    }

    try {
        // Get email
        $key=SERVERKEY.date("m.d.y");
        $email = JWT::decode($_POST['token'], $key);
        $auth = true;
    }
    catch (Exception $e) {  //hide $key on error
        http_response_code(400);
        $JsonReq = array('http_response_code' => 400, 'title' => 'Error', 'message' => 'Authentication error!!!');
        print json_encode($JsonReq);
        exit();
    }			

    if (!$auth) {
        http_response_code(400);
        $JsonReq = array('http_response_code' => 400, 'title' => 'Error', 'message' => 'Authentication error!!!');
        print json_encode($JsonReq);
        exit();
    }

    $identity=md5($email);

    //Connect to mysql
    $con1 = new mysqli(HOST, USERNAME, PWD, DB);
    if ($con1->connect_error) {
        http_response_code(400);
        $JsonReq = array('http_response_code' => 400, 'title' => 'Error', 'message' => "Connection Error" . $con1->connect_error);
        print json_encode($JsonReq);
        exit();
    }

    $Fld=$_POST['dataset'];
    if (!isset($Fld) || empty($Fld)) {
        http_response_code(201);
        $JsonReq = array('http_response_code' => 201, 'title' => 'Exclamation', 'message' => 'Please declare a dataset!!!');
        print json_encode($JsonReq);
        exit();
    }
    $Fld=$_POST['separator'];
    if (empty($Fld)) {
        http_response_code(201);
        $JsonReq = array('http_response_code' => 201, 'title' => 'Exclamation', 'message' => 'Please declare a seperator!!!');
        print json_encode($JsonReq);
        exit();
    }
    if (empty($_POST['min_support'])) {
        http_response_code(201);
        $JsonReq = array('http_response_code' => 201, 'title' => 'Exclamation', 'message' => 'Please declare minimum support!!!');
        print json_encode($JsonReq);
        exit();
    }
    if (empty($_POST['min_confidence'])) {
        http_response_code(201);
        $JsonReq = array('http_response_code' => 201, 'title' => 'Exclamation', 'message' => 'Please declare minimum confidence!!!');
        print json_encode($JsonReq);
        exit();
    }
    if (empty($_POST['min_lift'])) {
        http_response_code(201);
        $JsonReq = array('http_response_code' => 201, 'title' => 'Exclamation', 'message' => 'Please declare minimum lift!!!');
        print json_encode($JsonReq);
        exit();
    }    
    if (empty($_POST['max_length'])) {
        http_response_code(201);
        $JsonReq = array('http_response_code' => 201, 'title' => 'Exclamation', 'message' => 'Please declare maximum rule items!!!');
        print json_encode($JsonReq);
        exit();
    }

    $output = "python Python/Main02.py $identity ".$_POST['min_support']." ".$_POST['min_confidence']." ".$_POST['min_lift']." ".$_POST['max_length']." -3 ".$_POST['dataset']." ".$_POST['seperator']." 1 -2";
    //$output = passthru("python Python/Main02.py $identity ".$_POST['min_support']." ".$_POST['min_confidence']." ".$_POST['min_lift']." ".$_POST['max_length']." -3 ".$_POST['dataset']." ".$_POST['seperator']." 1 -2");
    http_response_code(200);
    $JsonReq = array('http_response_code' => 200, 'title' => 'Success', 'message' => $output);
    print json_encode($JsonReq);

?>