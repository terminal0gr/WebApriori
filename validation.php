<?php
	include("./config.php");
	include("./phpfunctions/jwt_helper.php");
	session_start(); 
	
   $con = new mysqli(HOST, USERNAME, PWD, DB);
   //$con = mysqli_connect("localhost", "webeng7", "webeng71819", "webeng7");
 
   /* check connection */
	if (mysqli_connect_errno()) {
		printf("<BR>Fatal Error: %s\n", mysqli_connect_error());
		exit();
	}
   
   $email = mysqli_real_escape_string($con, $_POST['email']);
   $passwd = mysqli_real_escape_string($con, $_POST['passwd']);
 
   $s="SELECT * FROM usertable WHERE email='$email'&& passwd=md5('$passwd')";
   $result = mysqli_query($con,$s);
   $num=mysqli_num_rows($result);
   
	// If result matched $myusername and $mypassword, table row must be 1 row
   if($num==1){

	   $token = array();
	   $token['id'] = $email;
	   $_SESSION["encodedToken"] = JWT::encode($token, SERVERKEY); //SERVERKEY from config.php

	   header("location:search.html");
	}else{
		
		$message = "Username and/or Password incorrect.\\nTry again.";
		echo "<script type='text/javascript'>alert('$message');
		window.location.href='Login.html';</script>";
		echo $message;

	}
//	session_destroy();
?>

