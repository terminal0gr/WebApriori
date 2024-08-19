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
        $email = (string) JWT::decode($_POST['token'], $key);
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

    $s="SELECT email FROM usertable WHERE email='$email'";
    $result = mysqli_query($con1,$s);
    $num=mysqli_num_rows($result);
    // If result matched $myusername and $mypassword, table row must be 1 row
    if($num!=1){
        http_response_code(400);
        $JsonReq = array('title' => 'Error', 'message' => 'Authentication error!!!');
        print json_encode($JsonReq);
        exit();
    }

    if (empty($_POST['dataset'])) {
        http_response_code(201);
        $JsonReq = array('title' => 'Exclamation', 'message' => 'Please declare a dataset!!!');
        print json_encode($JsonReq);
        exit();
    }

    $isPublic=0;
    //get dataset type is the first character of $_POST['dataset']
    if (substr($_POST['dataset'],0,2)=='p|') {
        // public dataset
        $isPublic=1;
        $filename=substr($_POST['dataset'],2);
    }else{
        // private dataset
        $isPublic=0;
        $filename=$_POST['dataset'];
    }

    if (empty($filename)) {
        http_response_code(201);
        $JsonReq = array('title' => 'Exclamation', 'message' => 'inadequate dataset file!!!');
        print json_encode($JsonReq);
        exit();
    }

    // File path where you want to write the JSON data
    // assemble output path
    if ($isPublic==0) {
        $fpatho="../Python/output/".$identity."/".$filename;
    } else {
        $fpatho="../Python/output/".$identity."/p/".$filename;            
    }
    $fpatho_parts = pathinfo($fpatho);
    $fpatho=$fpatho_parts['dirname']."/".$fpatho_parts['filename'].".epi";

    //Delete excluded participating items file
    if (file_exists($fpatho)) {
        if (!unlink($fpatho)) {
            echo "Error: Could not delete the file.";
            http_response_code(201);
            $JsonReq = array('title' => 'Exclamation', 'message' => 'Could not delete the previous excluded participating items!!!');
            print json_encode($JsonReq);
            exit();
        }
    } 

    if (empty($_POST['excludedParticipatingItems'])) {
        http_response_code(200);
        $JsonReq = array('title' => 'Information', 'message' => 'Participating items have been reinitialized successfully!');
        print json_encode($JsonReq);
        exit();
    }

    // Convert the PHP array to a JSON string
    //$json_string = json_encode($json_data, JSON_PRETTY_PRINT);
    $json_string=$_POST['excludedParticipatingItems'];

    //Write to file
    if (file_put_contents($fpatho, $json_string)) {
        http_response_code(200);
        $JsonReq = array('title' => 'Information', 'message' => 'Participating items have been saved successfully!');
        print json_encode($JsonReq);
    } else {
        http_response_code(201);
        echo "Error: Could not save the file.";
        $JsonReq = array('title' => 'Error', 'message' => 'Could not save the file!!!');
        print json_encode($JsonReq);
    }

    // //for debug purposes
    // http_response_code(201);
    // $JsonReq = array('title' => 'Debug', 'message' => $input);
    // print json_encode($JsonReq);
    exit();

?>
