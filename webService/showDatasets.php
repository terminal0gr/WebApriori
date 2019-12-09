<?php
    include("../phpfunctions/config.php");

    session_start(); 

    header('Content-Type: application/json');

    $auth = false;
    
    if (!isset($_POST['email'])) {
        http_response_code(400);
        $JsonReq = array('code' => 10, 'message' => 'Unauthorized!!!');
        print json_encode($JsonReq);
        exit();
    }

    if (!isset($_POST['apiKey'])) {
        http_response_code(400);
        $JsonReq = array('code' => 20, 'message' => 'Unauthorized!!!');
        print json_encode($JsonReq);
        exit();
    }

  	//Connect to mysql
    $con1 = new mysqli(HOST, USERNAME, PWD, DB);
	if ($con1->connect_error) {
        http_response_code(400);
        $JsonReq = array('code' => 30, 'message' => "Connection Error!!!");
        print json_encode($JsonReq);
        exit();
	}

    //The FILTER_SANITIZE_EMAIL filter removes all illegal characters from an email address
    $email = filter_var(trim($_POST["email"]), FILTER_SANITIZE_EMAIL);
    //mysqli_real_escape_string function is used to create a legal SQL string that you can use in an SQL statement.
	$email = mysqli_real_escape_string($con1, $_POST['email']);
    $apiKey = mysqli_real_escape_string($con1, $_POST['apiKey']);
    $identity=md5($email);

    if (empty($email) OR empty($apiKey) OR !filter_var($email, FILTER_VALIDATE_EMAIL)) {
        http_response_code(400);
        $JsonReq = array('code' => 40, 'message' => 'Unauthorized!!!');
        print json_encode($JsonReq);
        exit;
    }

    $s="SELECT key_created_at FROM usertable 
        WHERE email='$email' and webAPIKey='$apiKey'";
    $result = mysqli_query($con1,$s);
    $num=mysqli_num_rows($result);

    // If result matched $myusername and $mypassword, table row must be 1 row
    if(!$num==1){
        http_response_code(400);
        $JsonReq = array('code' => 50, 'message' => 'Unauthorized!!!');
        print json_encode($JsonReq);
        exit; 
    }

    $rowobj = $result->fetch_object();
    $dateTimestamp1=strtotime($rowobj->key_created_at);
    $dateTimestamp2=strtotime(date('Y/m/d'));
    if ($dateTimestamp1<$dateTimestamp2) {
        http_response_code(201);
        $JsonReq = array('code' => 60, 'message' => 'ApiKey expired!!!');
        print json_encode($JsonReq);
        exit; 
    }

    $filelist=array();
    for ($i = 1; $i < 5; $i++) {
        $log_directory="../Python/datasets/".$identity."/".$i."/";
        foreach(glob($log_directory.'*.*') as $file) {
            $filelist[] = array('datasetType' => $i, 'filename' => basename($file));
        };
    }
    if (count($filelist)>10) {
        $filelist=array_slice($filelist, 0, 10);
    }
    if($filelist) {
        http_response_code(200);
        if (count($filelist)==0) {
            exit();
        }
        print json_encode($filelist);
        exit();
    }
    
?>