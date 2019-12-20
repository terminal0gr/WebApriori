<?php
	include("config.php");
	include_once("functions.php");
	
	//session_start();
	$con1 = new mysqli(HOST, USERNAME, PWD, DB);
	
	/* check connection */
	if ($con1->connect_error) {
		die("Connection Error" . $con1->connect_error);
	}
		
	/* Connection succesful*/
	$confirm_code=mysqli_real_escape_string($con1, $_POST['passkey']);
	$passwd=mysqli_real_escape_string($con1, $_POST['passwd']);
	$query ="SELECT temail FROM temp_usertable WHERE confirm_code='$confirm_code'";
	$result = mysqli_query($con1,$query);
	$num=mysqli_num_rows($result);

	if (!$result) {
		echo "<script>alert('Unable to reset password!!!  Error(1). Please retry!!!');
		window.location.href='../index.html';
		</script>";
	}

	$row=mysqli_fetch_row($result);

	$email=$row[0];
	$passwd=md5($passwd);

	$sql="Update usertable set passwd='$passwd'
		  where email='$email'";
	$result = mysqli_query($con1,$sql);
	
	if (!$result) {
		echo "<script>alert('Unable to reset password!!!  Error(2). Please retry!!!');
		window.location.href='../index.html';
		</script>";
	}

	$sql="Delete 
	      From temp_usertable 
	      Where confirm_code='$confirm_code'";
	$result = mysqli_query($con1,$sql);

	if (!$result) {
		echo "<script>alert('Unable to reset password!!!  Error(3). Please retry!!!');
		window.location.href='../index.html';
		</script>";
	}

	echo "<script>alert('Your password has been successfully updated!!! Please Sign in.');
	sessionStorage.setItem('SignIn',true);
	window.location.href='../index.html';
	</script>";

?>

