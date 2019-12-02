<?php
    include("config.php");
	include("jwt_helper.php");
    session_start(); 
    
    $auth = false;

    if (!isset($_REQUEST['token'])) {
        http_response_code(400);
        echo('You are not signed in!!! Please sign in/up');
        exit();
    }

    try {
        // Get email
        $key=SERVERKEY.date("m.d.y");
        $email = JWT::decode($_REQUEST['token'], $key);
        $auth = true;
    }
    catch (Exception $e) {  //hide $key on error
        http_response_code(400);
        echo('Authentication error!!!');
        exit();
    }			

    if (!$auth) {
        http_response_code(400);
        echo('Authentication error!!!');
        exit();
    }

    $identity=md5($email);

    //Connect to mysql
    $con1 = new mysqli(HOST, USERNAME, PWD, DB);
    if ($con1->connect_error) {
        http_response_code(201);
        echo('Connection error!!!');
        exit();
    }

    if (!isset($_REQUEST['dataset'])) {
        http_response_code(201);
        echo('No filename has been provided!');
        exit();
    }
    
    if (!isset($_REQUEST['kind'])) {
        http_response_code(201);
        echo('Bad call arguments!');
        exit();
    }

    // Get parameters
    $postdata = urldecode($_REQUEST["dataset"]); // Decode URL-encoded string
    //get dataset type is the fisrt character of $_POST['dataset']
    $datasetType=substr($postdata,0,1);
    //get the filename
    $filename=substr($postdata,1);
    //Create dataset path
    $kind=$_REQUEST["kind"];

    $filepath='';
    if ($kind=='result') {
        $fpatho="../Python/output/".$identity."/".$datasetType."/".$filename;   
        $fpatho_parts = pathinfo($fpatho);
        $filepath=$fpatho_parts['dirname']."/".$fpatho_parts['filename'].".json";
    } elseif ($kind=='dataset') {
        $filepath="../Python/datasets/".$identity."/".$datasetType."/".$filename;   
    } else {
        http_response_code(201);
        echo('Bad call arguments!');
        exit();
    }

    // Process download
    if(file_exists($filepath)) {
        header('Content-Description: File Transfer');
        header('Content-Type: application/octet-stream');
        header('Content-Disposition: attachment; filename="'.basename($filepath).'"');
        header('Expires: 0');
        header('Cache-Control: must-revalidate');
        header('Pragma: public');
        header('Content-Length: ' . filesize($filepath));
        flush(); // Flush system output buffer
        readfile($filepath);
        exit;
    } 
?>