<?php
    include("config.php");
    include("jwt_helper.php");

    session_start(); 
    
    $auth = false;
	
    if (!isset($_FILES['fileToUpload'])) {
        http_response_code(400);
        $JsonReq = array('title' => 'Error', 'message' => 'No file for upload detected!!!');
        print json_encode($JsonReq);
        exit();
    }

    if (!isset($_POST['datasetType'])) {
        http_response_code(400);
        $JsonReq = array('title' => 'Error', 'message' => 'Dataset type not provided!!!');
        print json_encode($JsonReq);
        exit();
    }

    if (!isset($_POST['token'])) {
        http_response_code(400);
        $JsonReq = array('title' => 'Error', 'message' => 'You are not signed in!!! Please sign in/up');
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
        $JsonReq = array('title' => 'Error', 'message' => 'Authentication error!!!');
        print json_encode($JsonReq);
        exit();
    }			
        
    if (!$auth) {
        http_response_code(400);
        $JsonReq = array('title' => 'Error', 'message' => 'Authentication error!!!');
        print json_encode($JsonReq);
        exit();
    }

    $identity=md5($email);

  	//Connect to mysql
    $con1 = new mysqli(HOST, USERNAME, PWD, DB);
	if ($con1->connect_error) {
        http_response_code(400);
        $JsonReq = array('title' => 'Error', 'message' => "Connection Error" . $con1->connect_error);
        print json_encode($JsonReq);
        exit();
	}

    if ($_FILES["fileToUpload"]["error"] > 0) {
        http_response_code(201);
        $JsonReq = array('title' => 'Error', 'message' => 'Return Code: ' . $_FILES["fileToUpload"]["error"]);
        print json_encode($JsonReq);
        exit();
    }

    $filelist=array();
    $Vi=0;
    for ($i = 1; $i < 5; $i++) {
        $log_directory="../Python/datasets/".$identity."/".$i."/";
        foreach(glob($log_directory.'*.*') as $file) {
            $Vi++;
        };
    }
    if ($Vi>10) {
        http_response_code(201);
        $JsonReq = array('title' => 'exclamation', 'message' => 'Sorry, no more than 10 datasets are permitted per account!!!');
        print json_encode($JsonReq);
        exit();
    }

    $target_dir = "../Python/datasets/".$identity."/".$_POST['datasetType']."/";

    if (!is_dir($target_dir)) {
        if (!mkdir($target_dir, 0777, true)) {
            http_response_code(201);
            $JsonReq = array('title' => 'Error', 'message' => 'Failed to store file!');
            print json_encode($JsonReq);
            exit();
        }
    }

    $target_file = $target_dir . basename($_FILES["fileToUpload"]["name"]);
    //if file already exists
    if (file_exists($target_file)) {
        http_response_code(201);
        $JsonReq = array('title' => 'Exclamation', 'message' => $_FILES["fileToUpload"]["name"] . " already exists. ");
        print json_encode($JsonReq);
        exit();
    }
    else { //Store file 
        try {
            move_uploaded_file($_FILES["fileToUpload"]["tmp_name"], $target_file);

            http_response_code(200);
            $JsonReq = array('title' => 'Information', 'message' => 'File stored successfully.');
            print json_encode($JsonReq);
            exit();
        } catch (Exception $e) {
            http_response_code(400);
            $JsonReq = array('title' => 'Exception', 'message' =>'Caught exception: ',  $e->getMessage(), "\n");
            print json_encode($JsonReq);
            exit();
        }
    }
    
?>