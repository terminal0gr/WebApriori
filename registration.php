<?php
	session_start();
	$con1 = new mysqli("localhost", "webeng7", "webeng71819", "webeng7");
   
    /* check connection */
	if ($con1->connect_error)
		{
		die("Connection Error" . $con1->connect_error);
		}
		
	/* Connection succesful*/
	$confirm_code=md5(uniqid(rand()));
	$email = mysqli_real_escape_string($con1, $_POST['email']);
	$passwd =md5(mysqli_real_escape_string($con1, $_POST['passwd']));
	$oname = mysqli_real_escape_string($con1, $_POST['oname']);
	$fname = mysqli_real_escape_string($con1, $_POST['fname']);
	$query ="SELECT * FROM usertable WHERE email='$email'";
	$result = mysqli_query($con1,$query);
	$num=mysqli_num_rows($result);
	
	/* User is registered */
	if($num==1)
		{
		$message = "SORRY...YOU ARE ALREADY REGISTERED USER...";
		echo "<script type='text/javascript'>alert('$message');
		window.location.href='index.php';</script>";
		}
	/* New user @temp_usertable & send confirmation email */
	else
		{
		$sql="INSERT INTO temp_usertable(confirm_code,temail,tpasswd,toname,tfname)VALUES('$confirm_code','$email','$passwd','$oname','$fname')";
		$result = mysqli_query($con1,$sql);
		if($result)
			{
			$message = "Your Comfirmation link \r\nhttp://nireas.it.teithe.gr/webeng7/flights/confirmation.php?passkey=$confirm_code ";                   
			require_once("mailer/class.phpmailer.php");
			$mail = new PHPMailer;
			$mail -> IsSMTP();
			$mail->CharSet="UTF-8";       
			$mail->Host = 'smtp.teithe.gr';
			$mail->Port = 25;       
			$mail->From = 'ait242018@ait.teithe.gr';   
			$mail->FromName = 'Flights';
			$mail->addAddress($email);               
			$mail->Subject  = "Flights. Please verify!";
			$mail->Body  = $message;
			if(!$mail->send()) 
				{
				echo 'Το email δεν στάλθηκε.';
				echo 'Σφάλμα: ' . $mail->ErrorInfo;
				}
			else
				{			  
				$message = "Your Confirmation link Has Been Sent To Your Email Address.";
				echo "<script type='text/javascript'>alert('$message');
				window.location.href='Login.html';</script>";
				}
			}
		
		/* Confirmation email has been already sent */
		else
			{
			$message = "Your confirmation link has been already sent to your email address. Please check your email again!";
			echo "<script type='text/javascript'>alert('$message');
			window.location.href='Login.html';</script>";
			}
		}
 
	session_destroy();
?>
