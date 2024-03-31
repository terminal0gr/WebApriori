<?php
    include("config.php");
    include("jwt_helper.php");
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
        $email =(string) JWT::decode($_POST['token'], $key);
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

    $fpath="../Python/datasets/".$identity;
    if (!deleteDir($fpath)) {
        http_response_code(201);
        $JsonReq = array('title' => 'Error', 'message' => 'Could not delete user files 1!');
        print json_encode($JsonReq);
        exit();
    }
    $fpath="../Python/output/".$identity;
    if (!deleteDir($fpath)) {
        http_response_code(201);
        $JsonReq = array('title' => 'Error', 'message' => 'Could not delete user files 2!');
        print json_encode($JsonReq);
        exit();
    }
    $sql="DELETE from usertable WHERE email='$email'";
    $result = mysqli_query($con1,$sql);
    if (!$result) {
        http_response_code(201);
        $JsonReq = array('title' => 'Error', 'message' => 'Cannot delete user!');
        print json_encode($JsonReq);
        exit();
    }

    http_response_code(200);
    $JsonReq = array('title' => 'User deleted', 'message' => 'The user has been deleted.');
    print json_encode($JsonReq);  

?>