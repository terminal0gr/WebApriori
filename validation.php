<?php
   session_start(); 
 //   $con = new mysqli(HOST, USERNAME, PWD, DB);
 $con = new mysqli("localhost", "webeng7", "webeng71819", "webeng7");
 
 
        /* check connection */
	if (mysqli_connect_errno()) {
		printf("<BR>Αποτυχία Σύνδεσης: %s\n", mysqli_connect_error());
		exit();
	}
   
   $email = mysqli_real_escape_string($con, $_POST['email']);
   $passwd = mysqli_real_escape_string($con, $_POST['passwd']);
 
   $s="SELECT * FROM usertable WHERE email='$email'&& passwd=md5('$passwd')";
   $result = mysqli_query($con,$s);
   $num=mysqli_num_rows($result);
   
   
      // If result matched $myusername and $mypassword, table row must be 1 row

     
   if($num==1){
	 
	    $_SESSION['email']=$email;
	   header("location:search.php");
	}else{
		

		$message = "Username and/or Password incorrect.\\nTry again.";
		echo "<script type='text/javascript'>alert('$message');
		window.location.href='index.html';</script>";

		
	}
	session_destroy();
?>

