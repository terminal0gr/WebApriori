<?php
    include("../phpfunctions/config.php");
    include("../phpfunctions/functions.php");

    session_start(); 

    header('Content-Type: application/json');

    $auth = false;

    try {
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
            http_response_code(202);
            $JsonReq = array('code' => 40, 'message' => 'No dataset Id!!!');
            print json_encode($JsonReq);
            exit();
        }

        if (isset($_POST['email'])) {
            //The FILTER_SANITIZE_EMAIL filter removes all illegal characters from an email address
            $email = filter_var(trim($_POST["email"]), FILTER_SANITIZE_EMAIL);
            //mysqli_real_escape_string function is used to create a legal SQL string that you can use in an SQL statement.
            $email = mysqli_real_escape_string($con1, $email);
        }
        if (isset($_POST['apiKey'])) {$apiKey = mysqli_real_escape_string($con1, $_POST['apiKey']);}
        if (isset($_POST['separator'])) {$separator = escapeshellarg($_POST['separator']);}
        if (isset($_POST['min_support'])) {$min_support =escapeshellarg($_POST['min_support']);}
        if (isset($_POST['min_confidence'])) {$min_confidence =escapeshellarg($_POST['min_confidence']);}
        if (isset($_POST['min_lift'])) {$min_lift =escapeshellarg($_POST['min_lift']);}
        if (isset($_POST['max_length'])) {$max_length =escapeshellarg($_POST['max_length']);}

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

        if (empty($separator)) {
            http_response_code(201);
            $JsonReq = array('code' => 100, 'message' => 'no separator declared!!!');
            print json_encode($JsonReq);
            exit;
        }
        if (empty($min_support)) {
            http_response_code(201);
            $JsonReq = array('code' => 102, 'message' => 'no minimum support declared!!!');
            print json_encode($JsonReq);
            exit;
        }
        if (empty($min_confidence)) {
            http_response_code(201);
            $JsonReq = array('code' => 104, 'message' => 'no minimum confidence declared!!!');
            print json_encode($JsonReq);
            exit;
        }
        if (empty($min_lift)) {
            http_response_code(201);
            $JsonReq = array('code' => 106, 'message' => 'no minimum lift declared!!!');
            print json_encode($JsonReq);
            exit;
        }
        if (empty($max_length)) {
            http_response_code(201);
            $JsonReq = array('code' => 108, 'message' => 'no maximum rule items declared!!!');
            print json_encode($JsonReq);
            exit;
        }

        //get dataset type is the fisrt character of $_POST['dataset']
        if (substr($_POST['datasetId'],0,2)=='p|') {
            // public dataset
            $outputType=3;
            $datasetType=substr($_POST['datasetId'],2,1);
            $filename=substr($_POST['datasetId'],4);
        }else{
            // private dataset
            $outputType=2;
            $datasetType=substr($_POST['datasetId'],0,1);
            $filename=substr($_POST['datasetId'],2);
        }

        //Create dataset path
        if ($outputType==2) { //private dataset
            $fpath="../Python/datasets/".$identity."/".$datasetType."/".$filename;
        }else{ //public dataset
            $fpath="../Python/public/".$datasetType."/".$filename;            
        }

        if (!is_file($fpath)) {
            http_response_code(201);
            $JsonReq = array('code' => 110, 'message' => $fpath.'no dataset with this id found!!!');
            print json_encode($JsonReq);
            exit;
        }

        $input = 'python Main02.py ';
        $input.= '"'.$identity.'" ';
        $input.= $min_support.' ';
        $input.= $min_confidence.' ';
        $input.= $min_lift.' ';
        $input.= $max_length.' ';
        $input.= '"-3" ';
        $input.= escapeshellarg($filename).' ';
        $input.= $separator.' ';
        $input.= '"'.$datasetType.'" ';
        $input.= $outputType.' ';

        if (isset($_POST['extra_parameters'])) {
            $input.= $_POST['extra_parameters'];
        }

        
        if ($outputType==2) { //private dataset       
            $fpatho="../Python/output/".$identity."/".$datasetType."/".$filename;  
        }else{
            $fpatho="../Python/output/".$identity."/p".$datasetType."/".$filename;  
        }  
        $fpatho_parts = pathinfo($fpatho);
        $fpatho=$fpatho_parts['dirname']."/".$fpatho_parts['filename'].".json";
        if (is_file($fpatho)) {
            if (!unlink($fpatho)) {
                http_response_code(201);
                $JsonReq = array('code' => 112, 'message' => 'Could not delete old results for this dataset!!!');
                print json_encode($JsonReq);
                exit;
            }
        }

        //execure retrieval in Python
        chdir('../Python');
        execInBackground($input);

        http_response_code(200);
        $JsonReq = array('code' => 0 , 'message' => "Processing request...", 'datasetId' => $_POST['datasetId']);
        print json_encode($JsonReq);
        exit();  
    
    }
    catch (Exception $e) { 
        http_response_code(400);
        $JsonReq = array('code' => 999, 'message' => $e->getMessage());
        print json_encode($JsonReq);
        exit();
    }

?>