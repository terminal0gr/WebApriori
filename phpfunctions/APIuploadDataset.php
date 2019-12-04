<?php
    include("config.php");

    session_start(); 
    
    $auth = false;
	
    if (!isset($_FILES['fileToUpload'])) {
        http_response_code(400);
        $JsonReq = array('code' => 10, 'message' => 'No file for upload detected!!!');
        print json_encode($JsonReq);
        exit();
    }

    if (!isset($_POST['email'])) {
        http_response_code(400);
        $JsonReq = array('code' => 20, 'message' => 'Unauthorized!!!');
        print json_encode($JsonReq);
        exit();
    }

    if (!isset($_POST['apiKey'])) {
        http_response_code(400);
        $JsonReq = array('code' => 30, 'message' => 'Unauthorized!!!');
        print json_encode($JsonReq);
        exit();
    }

    if (!isset($_POST['datasetType'])) {
        http_response_code(400);
        $JsonReq = array('code' => 40, 'message' => 'Dataset type not provided!!!');
        print json_encode($JsonReq);
        exit();
    }

    if (!isset($_POST['fileName'])) {
        http_response_code(400);
        $JsonReq = array('code' => 50, 'message' => 'No filename Provided!!!');
        print json_encode($JsonReq);
        exit();
    }

  	//Connect to mysql
    $con1 = new mysqli(HOST, USERNAME, PWD, DB);
	if ($con1->connect_error) {
        http_response_code(400);
        $JsonReq = array('code' => 60, 'message' => "Connection Error!!!");
        print json_encode($JsonReq);
        exit();
	}

    if ($_FILES["fileToUpload"]["error"] > 0) {
        http_response_code(201);
        $JsonReq = array('code' => 70, 'message' => 'Return Code: ' . $_FILES["fileToUpload"]["error"]);
        print json_encode($JsonReq);
        exit();
    }

    //The FILTER_SANITIZE_EMAIL filter removes all illegal characters from an email address
    $email = filter_var(trim($_POST["email"]), FILTER_SANITIZE_EMAIL);
    //mysqli_real_escape_string function is used to create a legal SQL string that you can use in an SQL statement.
	$email = mysqli_real_escape_string($con, $_POST['email']);
    $apiKey = mysqli_real_escape_string($con, $_POST['apiKey']);
    $identity=md5($email);

    if (empty($email) OR empty($apiKey) OR !filter_var($email, FILTER_VALIDATE_EMAIL)) {
        http_response_code(400);
        $JsonReq = array('code' => 80, 'message' => 'Unauthorized!!!');
        print json_encode($JsonReq);
        exit;
    }

    $filelist=array();
    $Vi=0;
    for ($i = 1; $i < 5; $i++) {
        $log_directory="../Python/datasets/".$identity."/".$i."/";
        foreach(glob($log_directory.'*.*') as $file) {
            $Vi++;
        };
    }
    if ($Vi>MaxDatasets) {
        http_response_code(201);
        $JsonReq = array('code' => 90, 'message' => 'Sorry, no more than 10 datasets are permitted per account!!!');
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