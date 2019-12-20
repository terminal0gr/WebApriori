<?php
    include("config.php");
    include("jwt_helper.php");
    include_once("functions.php");

    session_start(); 
    
    $auth = false;
	
    if (!isset($_FILES['fileToUpload'])) {
        http_response_code(400);
        $JsonReq = array('title' => 'Error', 'message' => 'No file for upload detected!!!');
        print json_encode($JsonReq);
        exit();
    }

    if (!isset($_POST['datasetType'])) {
        http_response_code(400);
        $JsonReq = array('title' => 'Error', 'message' => 'Dataset type not provided!!!');
        print json_encode($JsonReq);
        exit();
    }

    if (!isset($_POST['isPublic'])) {
        http_response_code(400);
        $JsonReq = array('title' => 'Error', 'message' => 'Is public not provided!!!');
        print json_encode($JsonReq);
        exit();
    }
    $isPublic=$_POST['isPublic']=='true' ? TRUE : FALSE;

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
        $JsonReq = array('title' => 'Error (code 50)', 'message' => 'Authentication error!!!');
        print json_encode($JsonReq);
        exit();
    }			
        
    if (!$auth) {
        http_response_code(400);
        $JsonReq = array('title' => 'Error (code 60)', 'message' => 'Authentication error!!!');
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
    
    $s="SELECT CAST(grandPublicDatasets AS unsigned integer) as gPD FROM usertable WHERE email='$email'";
    $result = mysqli_query($con1,$s);
    $num=mysqli_num_rows($result);
    // If result matched $myusername and $mypassword, table row must be 1 row
    if($num!=1){
        http_response_code(400);
        $JsonReq = array('title' => 'Error (code 70)', 'message' => 'Authentication error!!!');
        print json_encode($JsonReq);
        exit();        
    }

    $rowobj = $result->fetch_object();

    if ($rowobj->gPD==0 && $isPublic) {
        http_response_code(201);
        $JsonReq = array('title' => 'Error (code 80)', 'message' => 'Authentication error!!!');
        print json_encode($JsonReq);
        exit();         
    }

    if ($_FILES["fileToUpload"]["error"] > 0) {
        http_response_code(201);
        $JsonReq = array('title' => 'Error', 'message' => 'Return Code: ' . $_FILES["fileToUpload"]["error"]);
        print json_encode($JsonReq);
        exit();
    }

    $filelist=array();
    $Vi=0;
    for ($i = 1; $i < 5; $i++) {
        $log_directory="../Python/datasets/".$identity."/".$i."/";
        foreach(glob($log_directory.'*.*') as $file) {
            $Vi++;
        };
    }
    if ($Vi>=MaxDatasets) {
        http_response_code(201);
        $JsonReq = array('title' => 'exclamation', 'message' => "Sorry, no more than ".MaxDatasets." datasets are permitted per account!!!");
        print json_encode($JsonReq);
        exit();
    }

    $target_dir = "../Python/datasets/".$identity."/".$_POST['datasetType']."/";
    if (!is_dir($target_dir)) {
        if (!mkdir($target_dir, 0777, true)) {
            http_response_code(201);
            $JsonReq = array('title' => 'Error code(90)', 'message' => 'Failed to store file!');
            print json_encode($JsonReq);
            exit();
        }
    }

    if ($isPublic) {
        $targetPbl_dir = "../Python/public/".$_POST['datasetType']."/";
        if (!is_dir($targetPbl_dir)) {
            if (!mkdir($targetPbl_dir, 0777, true)) {
                http_response_code(201);
                $JsonReq = array('title' => 'Error code(95)', 'message' => 'Failed to store file!');
                print json_encode($JsonReq);
                exit();
            }
        }
        $targetPbl_file = $targetPbl_dir . basename($_FILES["fileToUpload"]["name"]);
    }

    $target_file = $target_dir . basename($_FILES["fileToUpload"]["name"]);
    if (file_exists($target_file)) {
        http_response_code(201);
        $JsonReq = array('title' => 'Exclamation', 'message' => $_FILES["fileToUpload"]["name"] . " already exists.");
        print json_encode($JsonReq);
        exit();
    }

    if (isset($targetPbl_file)) {
        if ($isPublic) {
            if (file_exists($targetPbl_file)) { 
                http_response_code(201);
                $JsonReq = array('title' => 'Exclamation', 'message' => $isPublic.$_FILES["fileToUpload"]["name"] . " already exists in public directory.");
                print json_encode($JsonReq);
                exit();
            }
        }
    };

    //Store file. In case of public dataset it is stored in both private and public area because we count the datasets that resist in private area for comparing with MaxDatasets const
    try {
        move_uploaded_file($_FILES["fileToUpload"]["tmp_name"], $target_file);
        
        if ($isPublic) {copy($target_file, $targetPbl_file);};

        http_response_code(200);
        $JsonReq = array('title' => 'Information', 'message' => 'File stored successfully.');
        print json_encode($JsonReq);
        exit();
    } catch (Exception $e) {
        http_response_code(400);
        $JsonReq = array('title' => 'Exception', 'message' =>'Caught exception: ',  $e->getMessage(), "\n");
        print json_encode($JsonReq);
        exit();
    }
    
?>