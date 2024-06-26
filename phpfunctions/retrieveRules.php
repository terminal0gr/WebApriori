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
    if (empty($_POST['separator'])) {
        http_response_code(201);
        $JsonReq = array('title' => 'Exclamation', 'message' => 'Please declare a seperator!!!');
        print json_encode($JsonReq);
        exit();
    }
    if (empty($_POST['min_support'])) {
        http_response_code(201);
        $JsonReq = array('title' => 'Exclamation', 'message' => 'Please declare minimum support!!!');
        print json_encode($JsonReq);
        exit();
    }
    if (empty($_POST['min_confidence'])) {
        http_response_code(201);
        $JsonReq = array('title' => 'Exclamation', 'message' => 'Please declare minimum confidence!!!');
        print json_encode($JsonReq);
        exit();
    }
    if (empty($_POST['min_lift'])) {
        http_response_code(201);
        $JsonReq = array('title' => 'Exclamation', 'message' => 'Please declare minimum lift!!!');
        print json_encode($JsonReq);
        exit();
    }    
    if (empty($_POST['max_length'])) {
        http_response_code(201);
        $JsonReq = array('title' => 'Exclamation', 'message' => 'Please declare maximum rule items!!!');
        print json_encode($JsonReq);
        exit();
    }
    if (!isset($_POST['redundantType'])) {
        http_response_code(201);
        $JsonReq = array('title' => 'Exclamation', 'message' => 'Not redundant rules type declared!!!');
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

    // File path where you want to write the JSON data
    //assemble output path
    if ($isPublic==0) {
        $fpatho="../Python/output/".$identity."/".$filename;
    } else {
        $fpatho="../Python/output/".$identity."/p/".$filename;            
    }
    $fpatho_parts = pathinfo($fpatho);
    $fpatho=$fpatho_parts['dirname']."/".$fpatho_parts['filename'].".metadata";
    //I have to save the metadatafile here in case the user has customly changed dataset attributes
    $header1=filter_var($_POST['header1'], FILTER_VALIDATE_BOOLEAN);

    // Step 1: Read the JSON file
    $json_string = file_get_contents($fpatho);
    // Decode JSON data into a PHP array
    $json_data = json_decode($json_string, true);

    // Check if json_decode not succeeded
    if ($json_data === null && json_last_error() !== JSON_ERROR_NONE) {
        //Create new  $json_data
        $json_data = [
            "hasHeader"   => $header1,
            "delimiter"   => $_POST['separator'],
            "datasetType" => (int) $_POST['datasetType']
        ];

    }
    else {
        $json_data['hasHeader'] = $header1;
        $json_data['delimiter'] = $_POST['separator'];
        $json_data['datasetType'] = (int) $_POST['datasetType'];
    }

    $json_data['min_support']=0.01;
    if (!empty($_POST['min_support'])) {
        $json_data['min_support'] = (float) $_POST['min_support'];
    }
    $json_data['min_confidence']=0.2;
    if (!empty($_POST['min_confidence'])) {
        $json_data['min_confidence'] = (float) $_POST['min_confidence'];
    }
    $json_data['min_lift']=1.5;
    if (!empty($_POST['min_lift'])) {
        $json_data['min_lift'] = (float) $_POST['min_lift'];
    }
    $json_data['max_length']=4;
    if (!empty($_POST['max_length'])) {
        $json_data['max_length'] = (int) $_POST['max_length'];
    }
    $json_data['ssort']=-3; # order by lift descending
    if (!empty($_POST['ssort'])) {
        $json_data['ssort'] = (int) $_POST['ssort'];
    }
    $json_data['datasetName']=$filename;
    $json_data['public']=1; # 0=Private, 1=public
    if (!empty($_POST['public'])) {
        $json_data['public'] = (int) $_POST['public'];
    }    
    $json_data['redundantRemoveType']=0; # 0=No redunrtant, bitwise parameter
    if (!empty($_POST['redundantType'])) {
        $json_data['redundantRemoveType'] = (int) $_POST['redundantType'];
    }    
    $json_data['participatingItems']="[]"; 
    if (!empty($_POST['extra_parameters'])) {
        // Use a regular expression to match quoted segments
        preg_match_all('/"([^"]+)"/', $_POST['extra_parameters'], $matches);
        // Extract the matches
        $json_data['participatingItems'] = $matches[1];
        
        //$json_data['participatingItems'] = explode($_POST['separator'], str_replace('"', '', $_POST['extra_parameters']));
    }    

    // It is an append. the key/value pair is appended or, edited if it exists 
    if  ($json_data['datasetType']==2) { //2-INV dataset Type
        $json_data['groupItem']=(string) $_POST['groupItem'];
        $json_data['valueItem']=(string) $_POST['valueItem'];
    }

    if  ($json_data['datasetType']==3) { //3-SI dataset Type
        $json_data['absentValue']=(string) $_POST['absentValue'];
    }

    // Convert the PHP array to a JSON string
    $json_string = json_encode($json_data, JSON_PRETTY_PRINT);

    //Write to file
    file_put_contents($fpatho, $json_string);

    //Call Python for Association rules mining
    $input = PYTHON;
    $input.= ' Main05.py ';
    $input.= '"'.$identity.'" ';
    //$input.= '"'.$_POST['min_support'].'" ';
    //$input.= '"'.$_POST['min_confidence'].'" ';
    //$input.= '"'.$_POST['min_lift'].'" ';
    //$input.= '"'.$_POST['max_length'].'" ';
    //$input.= '"-3" ';
    $input.= '"'.$filename.'" ';
    $input.= '"'.$isPublic.'" ';
    //$input.= '"'.$_POST['redundantType'].'" ';
    //$input.= $_POST['extra_parameters'];

    // //for debug purposes
    // http_response_code(201);
    // $JsonReq = array('title' => 'Debug', 'message' => $input);
    // print json_encode($JsonReq);
    // exit();

    chdir('../Python');
    //asychronous call
    //exec($input.' > /dev/null 2>&1');
    //exec($input, $output);
    //alternative to exec


    //$input = escapeshellcmd($input);
    //$output = shell_exec($input);
    //echo $output;

    // http_response_code(200);
    // $JsonReq = array('title' => $input, 'message' => $output);
    // print json_encode($JsonReq);
    // exit();   

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
        $JsonReq = array('title' => $input, 'message' => substr($output,5), 'error_text'=>"Maximum association rules limit reached!!!($MaxRules). Please try adjusting minimum support, confidence or lift to reduce generated rules.");
    }
    else {
        $JsonReq = array('title' => $input, 'message' => $output);
    };
    print json_encode($JsonReq);
    exit();   

?>
