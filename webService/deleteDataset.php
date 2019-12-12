<?php
    include("../phpfunctions/config.php");

    session_start(); 

    header('Content-Type: application/json');

    $auth = false;
    
    if (!isset($_POST['email'])) {
        http_response_code(400);
        $JsonReq = array('code' => 10, 'message' => 'Unauthorized!!!');
        print json_encode($JsonReq);
        exit();
    }

    if (!isset($_POST['apiKey'])) {
        http_response_code(400);
        $JsonReq = array('code' => 20, 'message' => 'Unauthorized!!!');
        print json_encode($JsonReq);
        exit();
    }

  	//Connect to mysql
    $con1 = new mysqli(HOST, USERNAME, PWD, DB);
	if ($con1->connect_error) {
        http_response_code(400);
        $JsonReq = array('code' => 30, 'message' => "Connection Error!!!");
        print json_encode($JsonReq);
        exit();
	}

    if (!isset($_POST['datasetId'])) {
        http_response_code(201);
        $JsonReq = array('code' => 40, 'message' => 'No dataset Id declared!!!');
        print json_encode($JsonReq);
        exit();
    }

    //The FILTER_SANITIZE_EMAIL filter removes all illegal characters from an email address
    $email = filter_var(trim($_POST["email"]), FILTER_SANITIZE_EMAIL);
    //mysqli_real_escape_string function is used to create a legal SQL string that you can use in an SQL statement.
	$email = mysqli_real_escape_string($con1, $_POST['email']);
    $apiKey = mysqli_real_escape_string($con1, $_POST['apiKey']);
    $identity=md5($email);

    if (empty($email) OR empty($apiKey) OR !filter_var($email, FILTER_VALIDATE_EMAIL)) {
        http_response_code(400);
        $JsonReq = array('code' => 50, 'message' => 'Unauthorized!!!');
        print json_encode($JsonReq);
        exit;
    }

    $s="SELECT key_created_at FROM usertable 
        WHERE email='$email' and webAPIKey='$apiKey'";
    $result = mysqli_query($con1,$s);
    $num=mysqli_num_rows($result);

    // If result matched $myusername and $webAPIKey, table row must be 1 row
    if(!$num==1){
        http_response_code(400);
        $JsonReq = array('code' => 60, 'message' => 'Unauthorized!!!');
        print json_encode($JsonReq);
        exit; 
    }

    $rowobj = $result->fetch_object();
    $dateTimestamp1=strtotime($rowobj->key_created_at);
    $dateTimestamp2=strtotime(date('Y/m/d'));
    if ($dateTimestamp1<$dateTimestamp2) {
        http_response_code(201);
        $JsonReq = array('code' => 70, 'message' => 'ApiKey expired!!!');
        print json_encode($JsonReq);
        exit; 
    }

    //get dataset type is the fisrt character of $_POST['dataset']
    $datasetType=substr($_POST['datasetId'],0,1);
    //get the filename
    $filename=substr($_POST['datasetId'],2);
    //Create dataset path
    $fpath="../Python/datasets/".$identity."/".$datasetType."/".$filename;
    $message = '';
    if (is_file($fpath)) {
        if (!unlink($fpath)) {
            $message = "Could not delete dataset!!!\n";
        }
    } else {
        $message = "Could not find dataset!!!\n";
    }
    $fpatho="../Python/output/".$identity."/".$datasetType."/".$filename;   
    $fpatho_parts = pathinfo($fpatho);
    $fpatho=$fpatho_parts['dirname']."/".$fpatho_parts['filename'].".json";
    if (is_file($fpatho)) {
        if (!unlink($fpatho)) {
            $message = $message."Could not find/delete dataset results!!!\n";
        }
    }

    if ($message) {
        http_response_code(202);
        $JsonReq = array('code' => 70, 'message' => $message);
        print json_encode($JsonReq);
        exit();        
    }

    http_response_code(200);
    $JsonReq = array('code' => 0 , 'message' => "Dataset deleted successfully.");
    print json_encode($JsonReq);
    exit();  
    
?>