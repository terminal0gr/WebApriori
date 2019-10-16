<?php
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

    foreach(glob($log_directory.'/*.*') as $file) {
        $row = array();
        $row['datasetType'] = '1';
        $row['filename'] = $file;
        $filelist[] = $row;
    }
    http_response_code(200);
    print json_encode($filelist);
    exit();

?>