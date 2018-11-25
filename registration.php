<?php
	   session_start();
	    $con1 = new mysqli("localhost", "webeng7", "webeng71819", "webeng7");
   
        /* check connection */
    echo "preparing connection\n";    

if (!$con1) {
    echo "Error: Unable to connect to MySQL." . PHP_EOL;
    echo "Debugging errno: " . mysqli_connect_errno() . PHP_EOL;
    echo "Debugging error: " . mysqli_connect_error() . PHP_EOL;
}
	echo "Success: A proper connection to MySQL was made! The my_db database is great." . PHP_EOL;
	echo "Host information: " . mysqli_get_host_info($con1) . PHP_EOL;
    

    
   $confirm_code=md5(uniqid(rand()));
   
   $email = mysqli_real_escape_string($con1, $_POST['email']);
   $passwd =md5(mysqli_real_escape_string($con1, $_POST['passwd']));
   $oname = mysqli_real_escape_string($con1, $_POST['oname']);
   $fname = mysqli_real_escape_string($con1, $_POST['fname']);
   $query ="SELECT * FROM usertable WHERE email='$email'";
   $result = mysqli_query($con1,$query);
   $num=mysqli_num_rows($result);
   if($num==1){
	   
		$message = "SORRY...YOU ARE ALREADY REGISTERED USER...";
		echo "<script type='text/javascript'>alert('$message');
		window.location.href='index.php';</script>";
	}
	else
	{
	$sql="INSERT INTO temp_usertable(confirm_code,temail,tpasswd,toname,tfname)VALUES('$confirm_code','$email','$passwd','$oname','$fname')";
		$result = mysqli_query($con1,$sql);
		if($result){

			$to=$email;
			$subject="Your confirmation link here";
			$header="from: Flights";
			$message="Your Comfirmation link \r\n";
			$message.="Click on this link to activate your account \r\n";
			$message.="localhost/confirmation.php?passkey=$confirm_code";
			$sentmail = mail($to,$subject,$message,$header);
			}
			else {
				echo "Not found your email in our database";
			}
			if($sentmail){
				echo "Your Confirmation link Has Been Sent To Your Email Address.";
			}
			else {
				echo "Cannot send Confirmation link to your e-mail address";
			}

	}
   
   session_destroy();
   
	
		
		
   
?>
