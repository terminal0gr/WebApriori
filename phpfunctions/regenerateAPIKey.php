<?php
    include_once("config.php");
    include_once("jwt_helper.php");
    include_once("functions.php");
    
    session_start(); 
    
    $auth = false;

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
    };

    $identity=md5($email);

    //Connect to mysql
    $con1 = new mysqli(HOST, USERNAME, PWD, DB);
    if ($con1->connect_error) {
        http_response_code(201);
        $JsonReq = array('title' => 'Error', 'message' => "Connection Error" . $con1->connect_error);
        print json_encode($JsonReq);
        exit();
    };

    if ( empty($email) or !filter_var($email, FILTER_VALIDATE_EMAIL)) {
        http_response_code(400);
        $JsonReq = array('title' => 'Error', 'message' => 'Authentication error!!!');
        print json_encode($JsonReq);
        exit();
    };

    try {
        $key=generateRandomString(64);
        $date=date("d/m/Y");
        $sql="UPDATE usertable SET webAPIKey='$key', key_created_at=DATE_ADD(CURDATE(), INTERVAL 1 MONTH) WHERE email='$email'";
        $result = mysqli_query($con1,$sql);
        
        if (!$result) {
            http_response_code(400);
            $JsonReq = array('title' => 'Error', 'message' => 'Error writing to base!!!');
            print json_encode($JsonReq);
            exit();
        }

        $s="SELECT key_created_at FROM usertable WHERE email='$email'";
		$result = mysqli_query($con1,$s);
		$num=mysqli_num_rows($result);
		// If result matched $myusername and $mypassword, table row must be 1 row
		if($num!=1){
            http_response_code(400);
            $JsonReq = array('title' => 'Error', 'message' => 'Authentication error!!!');
            print json_encode($JsonReq);
            exit();
        }

        $row = $result->fetch_object();

        $date=date("d/m/Y");
        $date=$row->key_created_at;
        
        http_response_code(200);
        $JsonReq = array('title' => "Information" , 'message' => "New WebAPI key generated.", 'key' => $key, 'kdate' => $date);
        print json_encode($JsonReq);
        exit(); 

    }
    catch (Exception $e) { 
        http_response_code(400);
        $JsonReq = array('title' => 'Error', 'message' => $e->getMessage);
        print json_encode($JsonReq);
        exit();
    }
   
?>