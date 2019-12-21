<?php
    include_once("config.php");
    include_once("jwt_helper.php");
    include_once("functions.php");
    
    session_start(); 

    $auth = false;

    $inRecs = (array) json_decode(file_get_contents('php://input'), TRUE);
 
    if (!isset($inRecs["token"])) {
        http_response_code(400);
        $JsonReq = array('title' => 'Error', 'message' => 'You are not signed in!!! Please sign QQQ');
        print json_encode($JsonReq);
        exit();
    }

    try {
        // Get email
        $key=SERVERKEY.date("m.d.y");
        $email = JWT::decode($inRecs["token"], $key);
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

        $s="SELECT email, administrator
            FROM usertable 
            WHERE email='$email'";
		$result = mysqli_query($con1,$s);
		$num=mysqli_num_rows($result);

		// If result matched $myusername and $mypassword, table row must be 1 row
		if($num!=1){
            http_response_code(400);
            $JsonReq = array('title' => 'Error', 'message' => 'Authentication error!!!');
            print json_encode($JsonReq);
            exit();
        }

        $rowobj = $result->fetch_object();
        if ($rowobj->administrator!=1) {
            http_response_code(400);
            $JsonReq = array('title' => 'Error', 'message' => 'Authentication error!!!');
            print json_encode($JsonReq);
            exit();            
        }

        for ($i = 0; $i < count($inRecs['recs']); $i++) {
            $gPD=$inRecs['recs'][$i]['gPD'];
            $userEmail=$inRecs['recs'][$i]['email'];
            $sql="UPDATE usertable 
                  SET grandPublicDatasets=$gPD
                  WHERE email='$userEmail'";
            $result = mysqli_query($con1,$sql);
            if(!$result) {
                break;
            }
        }

        if($result) {
            http_response_code(200);
            $JsonReq = array('title' => 'Information', 'message' => 'Changes saved.');
            print json_encode($JsonReq);
            exit();
        }else{
            http_response_code(201);
            $JsonReq = array('title' => 'Error', 'message' => 'Database error!!!');
            print json_encode($JsonReq);
            exit();
        }

    }
    catch (Exception $e) { 
        http_response_code(400);
        $JsonReq = array('title' => 'Error', 'message' => $e->getMessage());
        print json_encode($JsonReq);
        exit();
    }

?>