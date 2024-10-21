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

    // File path where you want to write the JSON .metadata file
    ////////////////////////////////////////////////////////////
    ////////////////////////////////////////////////////////////
    //assemble output path
    if ($isPublic==0) {
        $fpatho="../Python/output/".$identity."/".$filename;
    } else {
        $fpatho="../Python/output/".$identity."/p/".$filename;            
    }
    $fpatho_parts = pathinfo($fpatho);
    $fpatho=$fpatho_parts['dirname']."/".$fpatho_parts['filename'].".metadata";
    //I have to save the metadatafile here in case the user has customly changed dataset attributes
    $hasHeader=filter_var($_POST['hasHeader'], FILTER_VALIDATE_BOOLEAN);

    // Step 1: Read the JSON file
    $json_string = file_get_contents($fpatho);
    // Decode JSON data into a PHP array
    $json_data = json_decode($json_string, true);

    // Check if json_decode not succeeded
    if ($json_data === null && json_last_error() !== JSON_ERROR_NONE) {
        //Create new  $json_data
        $json_data = [
            "hasHeader"   => $hasHeader,
            "delimiter"   => $_POST['delimiter'],
            "datasetType" => (int) $_POST['datasetType']
        ];
    }
    else {
        $json_data['hasHeader'] = $hasHeader;
        $json_data['delimiter'] = $_POST['delimiter'];
        if ($json_data['datasetType'] != (int) $_POST['datasetType']) {
            $json_data['datasetTypeChanged']=true;
        }
        $json_data['datasetType'] = (int) $_POST['datasetType'];
    }
    // The code below is not needed. Safe to delete after 30/03/2025
    // if ($json_data['datasetFeatures']) {
    //     if ($json_data['datasetFeatures']['delimiter']) {
    //         $json_data['datasetFeatures']['delimiter'][1]=$json_data['delimiter'];
    //         $json_data['datasetFeatures']['delimiter'][2]=$json_data['delimiter'];
    //     }
    //     if ($json_data['datasetFeatures']['hasHeader']) {
    //         $json_data['datasetFeatures']['hasHeader'][1]=$hasHeader;
    //         $json_data['datasetFeatures']['hasHeader'][2]=$hasHeader;
    //     }
    // }

    // It is an append. the key/value pair is appended or, edited if it exists 
    if  ($json_data['datasetType']==2) { //2-INV dataset Type
        // If groupItem or valueItem changed by user, then the dataset information features must be updated
        if ($json_data['groupItem'] != (string) $_POST['groupItem'] || $json_data['valueItem']!=(string) $_POST['valueItem']) {
            $json_data['datasetTypeChanged']=true;
        }
        $json_data['groupItem']=(string) $_POST['groupItem'];
        $json_data['valueItem']=(string) $_POST['valueItem'];
    }

    if  ($json_data['datasetType']==3) { //3-SI dataset Type
        // If absentValue changed by user, then the dataset information features must be updated
        if ($json_data['absentValue']!=(string) $_POST['absentValue']) {
            $json_data['datasetTypeChanged']=true;
        }
        $json_data['absentValue']=(string) $_POST['absentValue'];
    }

    // Convert the PHP array to a JSON string
    $json_string = json_encode($json_data, JSON_PRETTY_PRINT);

    //Write to file
    file_put_contents($fpatho, $json_string);
    // File path where you want to write the JSON .metadata file
    ////////////////////////////////////////////////////////////
    ////////////////////////////////////////////////////////////



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

    if (isJson($output)) {
        http_response_code(200);
        $jsonReq = json_decode($output, true);
        print json_encode($jsonReq);
    } else {
        http_response_code(201);
        $JsonReq = array('title' => 'The following error occured!', 'message' => $output);
        print json_encode($JsonReq);
    }
    exit();
    
?>