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
    if (empty($_POST['datasetType'])) {
        http_response_code(201);
        $JsonReq = array('title' => 'Exclamation', 'message' => 'inadequate dataset type!!!');
        print json_encode($JsonReq);
        exit();
    } else {
        if ((int) $_POST['datasetType']==3 && !isset($_POST['absentValue'])) {
            http_response_code(201);
            $JsonReq = array('title' => 'Exclamation', 'message' => 'You have not declared the absent item in 3-SI type dataset!!!');
            print json_encode($JsonReq);
            exit();
        }
        if ((int) $_POST['datasetType']==2 && !isset($_POST['groupItem'])) {
            http_response_code(201);
            $JsonReq = array('title' => 'Exclamation', 'message' => 'You have not declared the grouping item in 2-INV type dataset!!!');
            print json_encode($JsonReq);
            exit();
        }
        if ((int) $_POST['datasetType']==2 && !isset($_POST['valueItem'])) {
            http_response_code(201);
            $JsonReq = array('title' => 'Exclamation', 'message' => 'You have not declared the value item in 2-INV type dataset!!!');
            print json_encode($JsonReq);
            exit();
        }
    }

    $reInitialize=false;
    if (!empty($_POST['reInitialize'])) {
        $reInitialize=$_POST['reInitialize'];
    }
    
    if ($reInitialize) {
        if ($isPublic==0) {
            $fpatho="../Python/output/".$identity."/".$filename;
        } else {
            $fpatho="../Python/output/".$identity."/p/".$filename;            
        }
        $fpatho_parts = pathinfo($fpatho);
        $fpatho=$fpatho_parts['dirname']."/".$fpatho_parts['filename'].".epi";
        unlink($fpatho);
    }         

    //Call Python for Association rules mining
    $input = PYTHON;
    $input.= ' Main05.py ';
    $input.= '"'.$identity.'" ';
    $input.= '"'.$filename.'" ';
    $input.= '"'.$isPublic.'" ';
    $input.= '"1" ';
    if ((int) $_POST['datasetType']==2 && isset($_POST['groupItem'])) {
        $input.= '"'.$_POST['groupItem'].'" ';
    }
    if ((int) $_POST['datasetType']==2 && isset($_POST['valueItem'])) {
        $input.= '"'.$_POST['valueItem'].'" ';
    }
    if ((int) $_POST['datasetType']==3 && isset($_POST['absentValue'])) {
        $input.= '"'.$_POST['absentValue'].'" ';
    }


    // //for debug purposes
    // http_response_code(201);
    // $JsonReq = array('title' => 'Debug', 'message' => $input);
    // print json_encode($JsonReq);
    // exit();

    chdir('../Python');
 
    try {
        set_time_limit(1800); //in seconds
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
        $JsonReq = array('title' => 'Invalid parameters! Please check!<br><br>', 'message' => $input);
        print json_encode($JsonReq);
        exit();
    }
    elseif (strpos($output, 'error occurred') !== false) {
        http_response_code(201);
        $JsonReq = array('title' => 'Error!', 'message' => 'parameters:<br>'.$input.'.<br><br> Error:<br>'.$output);
        echo json_encode($JsonReq);
        exit();
    }

    http_response_code(200);
    if (substr($output, 0, 1)=='@') {
        $MaxRules=intval(substr($output, 1, 4));
        $JsonReq = array('title' => $input, 'message' => substr($output,5), 'error_text'=>"Maximum items limit reached!!! ($MaxItems). Onle the first $MaxItems will be participating in Association Rules Mining!");
    }
    else {
        $JsonReq = array('title' => $input, 'message' => $output);
    };
    print json_encode($JsonReq);
    exit();   

?>
