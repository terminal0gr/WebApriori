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

    $forceAutoDetect=false;
    if (isset($_POST['forceAutoDetect'])) {
        $forceAutoDetect=filter_var($_POST['forceAutoDetect'], FILTER_VALIDATE_BOOLEAN);
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
    
    //get dataset type is the first character of $_POST['dataset']
    if (substr($_POST['dataset'],0,2)=='p|') {
        // public dataset
        $isPublic=1;
        $datasetType=substr($_POST['dataset'],2,1);
        $filename=substr($_POST['dataset'],3);
    }else{
        // private dataset
        $isPublic=0;
        $datasetType=substr($_POST['dataset'],0,1);
        $filename=substr($_POST['dataset'],1);
    }


    //Read dataset's attributes from save file (dataset).metadata and not autodetect
    if (!$forceAutoDetect) {

        //assemble output path
        if ($isPublic==0) {
            $fpatho="../Python/output/".$identity."/".$datasetType."/".$filename;
        } else {
            $fpatho="../Python/output/".$identity."/p".$datasetType."/".$filename;            
        }
        $fpatho_parts = pathinfo($fpatho);
        $fpatho=$fpatho_parts['dirname']."/".$fpatho_parts['filename'].".metadata";
        $message = '';

        if (is_file($fpatho)) {
            try {
                $json = file_get_contents($fpatho);
                $jsonReq = json_decode($json, true);
                http_response_code(200);
                print json_encode($jsonReq);
                exit();
            }
            catch (Exception $e) {  
                $forceAutoDetect=true;
            }	
        } else {
            $forceAutoDetect=true;
        }
    }



    if (!$forceAutoDetect) {
        exit();
    }

    $input = PYTHON;
    $input.= ' DatasetAttrAutoDetect.py ';
    $input.= '"'.$identity.'" ';
    $input.= '"'.$filename.'" ';
    $input.= '"'.$datasetType.'" ';
    $input.= '"'.$isPublic.'"';

    chdir('../Python');

    try {
        set_time_limit(60); //in seconds
        ob_start();
        passthru($input);
        $output = ob_get_contents();
        ob_end_clean();
    } catch (Exception $e) {
        http_response_code(201);
        $JsonReq = array('title' => $input.'Error', 'message' => $e->getMessage());
        print json_encode($JsonReq);
        exit();
    }

    if (!$output) {
        http_response_code(201);
        $JsonReq = array('title' => 'Invalid parameters! Please check!', 'message' => $input);
        print json_encode($JsonReq);
        exit();
    }

    http_response_code(200);
    $jsonReq = json_decode($output, true);
    print json_encode($jsonReq);
    
    exit();

?>