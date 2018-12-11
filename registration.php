<?php
	session_start();
	$con1 = mysqli_connect("localhost", "webeng7", "webeng71819", "webeng7");

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
	
	
	// Check captcha
	$captcha_error = "";
	$captcha = $_POST['g-recaptcha-response'];
	if (!isset($_POST['g-recaptcha-response'])||empty($_POST['g-recaptcha-response'])) {
        $captcha_error = "Δεν έχετε κάνει τον έλεγχο επαλήθευσης";
	} else {
		$response = file_get_contents("https://www.google.com/recaptcha/api/siteverify?secret=X6LdP7H8UAAAAAFZ5qAl0_FmLAqzdBUeD0G3ZaX0p&response=".$_POST['g-recaptcha-response'], False);
		
		$jresponse = json_decode($response, true);
		if(!$jresponse["success"] === true)
		{
			$captcha_error = "Δεν πέτυχε ο έλεγχος επαλήθευσης";//.$response;
		}
	}
	if($captcha_error != "") {
		echo "<script type='text/javascript'>alert('$captcha_error');
		window.location.href='SignUp.html';</script>";
	}
	
	
	
	/* User is registered */
	if($num==1)
		{
		$message = "SORRY...YOU ARE ALREADY REGISTERED USER...";
		echo "<script type='text/javascript'>alert('$message');
		window.location.href='SignUp.html';</script>";
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
			$mail->Subject  = "Flights Scanner. Please verify!";
			$mail->Body  = $message;
			if(!$mail->send()) 
				{
				echo 'Email has not been sent.';
				echo 'Errot: ' . $mail->ErrorInfo;
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
