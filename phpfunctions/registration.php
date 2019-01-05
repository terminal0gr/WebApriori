<?php
	include("config.php");
	
	session_start();
	$con1 = new mysqli(HOST, USERNAME, PWD, DB);
	
	/* check connection */
	if ($con1->connect_error) {
		http_response_code(403);
		$JsonReq = array('http_response_code' => 201, 'title' => 'Error', 'message' => 'Connection Error');
		print json_encode($JsonReq);
		die("Connection Error" . $con1->connect_error);
	}
	
	//erase expired orphan records
	$sql="DELETE FROM temp_usertable WHERE `created_at`<DATE_SUB(NOW(), INTERVAL 5 MINUTE)";
	$result = mysqli_query($con1,$sql);

	// Check captcha
	$captcha_error = "";
	$captcha = $_POST['g-recaptcha-response'];
	
	if (!isset($_POST['g-recaptcha-response'])||empty($_POST['g-recaptcha-response'])) {
        $captcha_error = "Verification check has not been done";
	} else {
		$response = file_get_contents("https://www.google.com/recaptcha/api/siteverify?secret=6LdP7H8UAAAAAFZ5qAl0_FmLAqzdBUeD0G3ZaX0p&response=".$_POST['g-recaptcha-response'], False);
		
		$jresponse = json_decode($response, true);
		if(!$jresponse["success"] === true)
		{
			$captcha_error = true;
			echo "<script type='text/javascript'>alert('Verification check failed');
			window.location.href='../SignUp.html';</script>";
		}
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
	if($num==1) {
		http_response_code(201);
		$JsonReq = array('http_response_code' => 201, 'title' => 'Warning', 'message' => 'Sorry...You are already registered user...');
		print json_encode($JsonReq);
	} elseif(!$captcha_error) { /* New user @temp_usertable & send confirmation email */
		$sql="INSERT INTO temp_usertable(confirm_code,temail,tpasswd,toname,tfname)VALUES('$confirm_code','$email','$passwd','$oname','$fname')";
		$result = mysqli_query($con1,$sql);
		
		if($result) {
			$message = "Your Confirmation link \r\nhttp://nireas.it.teithe.gr/webeng7/flights/phpfunctions/confirmation.php?passkey=$confirm_code ";                   
			require_once("class.phpmailer.php");
			$mail = new PHPMailer;
			$mail -> IsSMTP();
			$mail->CharSet="UTF-8";       
			$mail->Host = 'smtp.teithe.gr';
			$mail->Port = 25;       
			$mail->From = 'ait242018@ait.teithe.gr';   
			$mail->FromName = 'Flights';
			$mail->addAddress($email);               
			$mail->Subject  = "Flights Scanner. Please confirm your verification!";
			$mail->Body  = $message;
			if(!$mail->send()) {

				http_response_code(403);
				$JsonReq = array('http_response_code' => 201, 'title' => 'Error', 'message' => 'Email has not been sent.' + $mail->ErrorInfo);
				print json_encode($JsonReq);
				exit();
			} else {			  

				http_response_code(200);
				$JsonReq = array('http_response_code' => 200, 'title' => 'Information', 'message' => 'Your Confirmation link Has Been Sent To Your Email Address.');
				print json_encode($JsonReq);
				exit();

			}
		} else { /* Confirmation email has been already sent */
			http_response_code(403);
			$JsonReq = array('http_response_code' => 201, 'title' => 'Information', 'message' => 'Your confirmation link has been already sent to your email address '.$email.'. Please check your email again!');
			print json_encode($JsonReq);
			exit();

		}
	}
 
	session_destroy();
?>
