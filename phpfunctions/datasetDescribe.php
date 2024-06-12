<?php
    include("config.php");
    include("jwt_helper.php");
    include_once("functions.php");
    header('Content-Type: application/json');
    
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
        http_response_code(201);
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

    if (!isset($_POST['dataset'])) {
        http_response_code(201);
        $JsonReq = array('title' => 'Error', 'message' => 'No dataset name has been declared!');
        print json_encode($JsonReq);
        exit();
    }

    $isPublic=0;
    $fPathI="";
    //get dataset type is the first character of $_POST['dataset']
    if (substr($_POST['dataset'],0,2)=='p|') {
        // public dataset
        $isPublic=1;
        $filename=substr($_POST['dataset'],2);
        $fPathI="../Python/output/".$identity."/p/".$filename;     
    }else{
        // private dataset
        $isPublic=0;
        $filename=$_POST['dataset'];
        $fPathI="../Python/output/".$identity."/".$filename;
    }

    if (empty($filename)) {
        http_response_code(201);
        $JsonReq = array('title' => 'Exclamation', 'message' => 'inadequate dataset file!!!');
        print json_encode($JsonReq);
        exit();
    }

    $rows=10;
    if (isset($_POST['rows'])) {
        $rows=$_POST['rows'];
    }
    $columns=15;
    if (isset($_POST['columns'])) {
        $columns=$_POST['columns'];
    }

    //Call datasetDescribe.py
    $input = PYTHON;
    $input.= ' datasetDescribe.py ';
    $input.= '"'.$identity.'" ';
    $input.= '"'.$filename.'" ';
    $input.= '"'.$rows.'" ';
    $input.= '"'.$columns.'" ';
    $input.= '"'.$isPublic.'" ';

    try {
        chdir('../Python');
        set_time_limit(20); //in seconds
        ob_start();
        passthru($input);
        $output = ob_get_contents();
        ob_end_clean();
    } catch (Exception $e) {
        http_response_code(201);
        $JsonReq = array('title' => ' Error! '.$input, 'message' => $e);
        print json_encode($JsonReq);
        exit();
    }

    if (!$output) {
        http_response_code(201);
        $JsonReq = array('title' => 'Error!', 'message' => 'parameters:<br>'.$input.'.<br><br>Python did not resonded for unknown reason.');
        echo json_encode($JsonReq);
        exit();
    }
    elseif (strpos($output, 'error occurred') !== false) {
        http_response_code(201);
        $JsonReq = array('title' => 'Error!', 'message' => 'parameters:<br>'.$input.'.<br><br>Error:<br>'.$output);
        echo json_encode($JsonReq);
        exit();
    }

    http_response_code(200);
    print json_encode($output);
    exit();  
?>