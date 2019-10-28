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

    if (empty($_POST['dataset'])) {
        http_response_code(201);
        $JsonReq = array('http_response_code' => 201, 'title' => 'Exclamation', 'message' => 'Please declare a dataset!!!');
        print json_encode($JsonReq);
        exit();
    }
    if (empty($_POST['separator'])) {
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

    //pathinfo path and name info
    $prmFile = pathinfo($_POST['dataset']);
    //get the filename
    $filename=basename($_POST['dataset']);
    //get the last folder from the path
    $datasetType=basename($prmFile['dirname']);

    if (empty($filename)) {
        http_response_code(201);
        $JsonReq = array('http_response_code' => 201, 'title' => 'Exclamation', 'message' => 'inadequate dataset file!!!');
        print json_encode($JsonReq);
        exit();
    }
    if (empty($datasetType)) {
        http_response_code(201);
        $JsonReq = array('http_response_code' => 201, 'title' => 'Exclamation', 'message' => 'inadequate dataset type!!!');
        print json_encode($JsonReq);
        exit();
    }
    else {
        switch($datasetType) {
            case '1';
            case '2';
            case '3';
            case '4';
            break;        
        default;
            http_response_code(201);
            $JsonReq = array('http_response_code' => 201, 'title' => 'Exclamation', 'message' => 'inadequate dataset!!!');
            print json_encode($JsonReq);
            exit();
        }
    }

    $input = "python Main02.py $identity ".$_POST['min_support']." ".$_POST['min_confidence']." ".$_POST['min_lift']." ".$_POST['max_length']." -3 ".$filename." ".$_POST['separator']." ".$datasetType." -1";

    chdir('../Python');
    //asychronous call
    //exec($input.' > /dev/null 2>&1 &');
    exec($input, $output);
    //exec($input);
    //alternative to exec
    //$output = passthru($input);
    http_response_code(200);
    $JsonReq = array('http_response_code' => 200, 'title' => 'ok', 'message' => $output);
    print json_encode($JsonReq);
    exit();   


?>