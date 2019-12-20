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

    if ( empty($email) or !filter_var($email, FILTER_VALIDATE_EMAIL)) {
        http_response_code(400);
        $JsonReq = array('title' => 'Error', 'message' => 'Authentication error!!!');
        print json_encode($JsonReq);
        exit();
    }

    try {
        $s="SELECT email, fname, oname, CAST(grandPublicDatasets AS unsigned integer) as gPD FROM usertable WHERE email='$email'";
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

        
        
    }
    catch (Exception $e) { 
        http_response_code(400);
        $JsonReq = array('title' => 'Error', 'message' => $e->getMessage());
        print json_encode($JsonReq);
        exit();
    }

    http_response_code(200);
    $JsonReq = array('title' => "Information" , 'message' => "New WebAPI key generated.", 'srv' => siteRoot, 'email' => $email, 'key' => $key, 'kdate' => $date);
    print json_encode($JsonReq);
    exit(); 
    
?>