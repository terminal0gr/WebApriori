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
        $JsonReq = array('title' => 'Error (code 70)', 'message' => 'Authentication error!!!');
        print json_encode($JsonReq);
        exit();        
    }

    if (!isset($_POST['dataset'])) {
        http_response_code(201);
        $JsonReq = array('title' => 'Error', 'message' => 'No dataset name has been declared!');
        print json_encode($JsonReq);
        exit();
    }

    //get dataset type is the fisrt character of $_POST['dataset']
    if (substr($_POST['dataset'],0,2)=='p|') {
        // public dataset
        $outputType=3;
        $filename=substr($_POST['dataset'],2);
    }else{
        // private dataset
        $outputType=2;
        $filename=$_POST['dataset'];
    }

    //Create dataset path
    if ($outputType==2) {
        //private dataset
        $fpath="../Python/datasets/".$identity."/".$filename;
    }else{
        //public dataset
        $fpath="../Python/public/".$filename;   
    }

    $message = '';
    if (is_file($fpath)) {
        if (!unlink($fpath)) {
            $message = "Could not delete dataset!!!\n";
        }
    } else {
        $message = "Could not find dataset!!!\n";
    }

    if ($outputType==2) {
        $fpatho="../Python/output/".$identity."/".$filename;
    }else{
        $fpatho="../Python/output/".$identity."/p".$filename;
    } 
      
    $fpatho_parts = pathinfo($fpatho);
    $fpatho=$fpatho_parts['dirname']."/".$fpatho_parts['filename'].".json";
    if (is_file($fpatho)) {
        if (!unlink($fpatho)) {
            $message = $message."Could not find/delete dataset results!!!\n";
        }
    }

    if ($message) {
        http_response_code(201);
        $JsonReq = array('title' => "exclamation" , 'message' => $message);
        print json_encode($JsonReq);
        exit();        
    }

    http_response_code(200);
    $JsonReq = array('title' => "Information" , 'message' => "Dataset removed successfully.");
    print json_encode($JsonReq);
    exit();  
?>