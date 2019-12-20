<?php
	include("config.php");
	include("jwt_helper.php");
	include_once("functions.php");
	
	session_start();
	$con1 = new mysqli(HOST, USERNAME, PWD, DB);
	
	/* check connection */
	if ($con1->connect_error) {
		die("Connection Error" . $con1->connect_error);
	}
		
	try {
		// Get email
		if (isset($_POST['token'])) {
			$key=SERVERKEY.date("m.d.y");
			$voldemail = JWT::decode($_POST['token'], $key);
		}else {
			http_response_code(400);
			$JsonReq = array('title' => 'Error', 'message' => 'Authentication error...');
			print json_encode($JsonReq);
			exit();
		}
	}
	catch (Exception $e) {  //hide $key on error
		http_response_code(400);
		$JsonReq = array('title' => 'Error', 'message' => 'Authentication error...');
		print json_encode($JsonReq);
		exit();
	}	

	$oldemail=mysqli_real_escape_string($con1, $_POST['oldemail']);
	if ($oldemail!=$voldemail) {
		http_response_code(400);
		$JsonReq = array('title' => 'Error', 'message' => 'Authentication error...');
		print json_encode($JsonReq);
		exit();
	}

	$email = mysqli_real_escape_string($con1, $_POST['email']);

	unset($passwd);

	if (isset($_POST['passwd']) && trim($_POST['passwd'])!='') {
		$passwd =md5(mysqli_real_escape_string($con1, $_POST['passwd']));
	}
	$oname = mysqli_real_escape_string($con1, $_POST['oname']);
	$fname = mysqli_real_escape_string($con1, $_POST['fname']);

	$query ="SELECT * FROM usertable WHERE email='$oldemail'";
	$result = mysqli_query($con1,$query);
	$num=mysqli_num_rows($result);
	
	/* User is registered */
	if($num==0) {
		http_response_code(201);
		$JsonReq = array('title' => 'Error', 'message' => 'Sorry...You are not a registered user...');
		print json_encode($JsonReq);
		exit();
	}

	$Stfields="email='$email'";

	$rowobj = $result->fetch_object();
	if (isset($passwd)) {
		if ($rowobj->passwd==$passwd) {
			http_response_code(201);
            $JsonReq = array('title' => 'Information', 'message' => 'Sorry...you have used that password...');
            print json_encode($JsonReq);
			exit();
		}
		$Stfields.=",passwd='$passwd'";
	}

	$Stfields.=",oname='$oname'";
	$Stfields.=",fname='$fname'";

	$sql="UPDATE usertable SET $Stfields WHERE email='$oldemail'";
	$result = mysqli_query($con1,$sql);
		
	if($result) {
		$sql="SELECT * FROM usertable WHERE email='$email'";
		$result = mysqli_query($con1,$sql);
		$num=mysqli_num_rows($result);

		if($num==1){

            $rowobj = $result->fetch_object();

			$token = array();
			$token['id'] = $email;
			$key=SERVERKEY.date("m.d.y");

			http_response_code(200);
            $JsonReq = array('token' => JWT::encode($email, $key), 'name' => $rowobj->fname." ".$rowobj->oname, 'message' => 'success');
            print json_encode($JsonReq);

		} else {
			//set a 403 (forbidden) response code.	
			http_response_code(403);
            $JsonReq = array('title' => 'Error', 'message' => 'Authentication error occured');
            print json_encode($JsonReq);
			exit();
		}

	}
 
	session_destroy();
?>
