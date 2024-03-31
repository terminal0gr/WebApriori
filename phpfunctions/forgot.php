<?php
	include("config.php");
	
	//Import the PHPMailer class into the global namespace
	require './PHPMailer/src/PHPMailer.php';
	require './PHPMailer/src/Exception.php';
	require './PHPMailer/src/SMTP.php';
	use PHPMailer\PHPMailer\PHPMailer;
	use PHPMailer\PHPMailer\Exception;

	session_start();
	$con1 = new mysqli(HOST, USERNAME, PWD, DB);
	
	/* check connection */
	if ($con1->connect_error) {
		die("Connection Error" . $con1->connect_error);
	}
		
	//erase expired orphan records
	$sql="DELETE FROM temp_usertable WHERE `created_at`<DATE_SUB(NOW(), INTERVAL 5 MINUTE)";
	$result = mysqli_query($con1,$sql);

	// Check captcha
	$captcha_error = "";
	try {
		if (isset($_POST['g-recaptcha-response'])) {
			$captcha = $_POST['g-recaptcha-response'];
		}else{
			$captcha_error = true;
			echo "<script type='text/javascript'>alert('Verification check failed');window.location.href='../SignUp.html';</script>";
			exit();
		}
	}catch (Exception $e) {  
		$captcha_error = true;
		echo "<script type='text/javascript'>alert('Verification check failed');window.location.href='../SignUp.html';</script>";
		exit();
    }	
	
	if (!isset($_POST['g-recaptcha-response'])||empty($_POST['g-recaptcha-response'])) {
		echo "<script type='text/javascript'>alert('Verification check failed');window.location.href='../SignUp.html';</script>";
		exit();
	} else {
		$response = file_get_contents("https://www.google.com/recaptcha/api/siteverify?secret=6LfbnNgUAAAAAALlBsuZoP6hjYvU98Utv1epeyqh&response=".$_POST['g-recaptcha-response'], False);
		
		$jresponse = json_decode($response, true);
		if(!$jresponse["success"] === true)
		{
			$captcha_error = true;
			echo "<script type='text/javascript'>alert('Verification check failed');
			window.location.href='../SignUp.html';</script>";
			exit();
		}
	}
	
	if(!$captcha_error) { 
		
		$email = mysqli_real_escape_string($con1, $_POST['email']);
		$query ="SELECT * FROM usertable WHERE email='$email'";
		$result = mysqli_query($con1,$query);
		$num=mysqli_num_rows($result);
        
		if($result) {

            if($num==1) {

				$query ="SELECT * FROM temp_usertable WHERE temail='$email'";
				$result = mysqli_query($con1,$query);
				$num=mysqli_num_rows($result);

				if ($num>0) {
					$message = "The confirmation link has already been sent to your email address ".$email.". Please check your email or retry in 5 minutes";
					echo "<script>alert('$message');
					window.location.href='../index.html';
					</script>";
					exit();
				}

				$confirm_code=md5(uniqid(rand()));

                $sql="INSERT INTO `temp_usertable` (`confirm_code`, `temail`, `tpasswd`, `toname`, `tfname`)
                     values ('$confirm_code', '$email' ,'','','')";
                $result = mysqli_query($con1,$sql);

				$mail = new PHPMailer(TRUE);
				$mail->IsSMTP();
				$mail->CharSet="UTF-8";     
				$mail->Host = smtpHost;
				$mail->Port = smtpPort; 
				if (defined('smtpAuth')) {$mail->SMTPAuth = smtpAuth;};           
				if (defined('smtpUsername')) {$mail->Username = smtpUsername;};  
				if (defined('smtpPassword')) {$mail->Password = smtpPassword;};   
				if (defined('smtpSecure')) {$mail->SMTPSecure = smtpSecure;};
				if (defined('smtpFrom') && defined('smtpFromName')) {$mail->setFrom(smtpFrom, smtpFromName);};
                $mail->addAddress($email);               
				$mail->Subject  = "WebApriori. Reset password";
				$mail->Body  = 	
				"<p>WebApriori association rules mining reset password procedure.</p>
				<br>
				<h2>Click <a href=\"{$_SERVER['SERVER_NAME']}/phpfunctions/forgot1.php?passkey=$confirm_code\">here</a></h2>
				<h2>Or as an alternative, copy & paste the link above to your explorer</h2>
				<h2>{$_SERVER['SERVER_NAME']}/phpfunctions/forgot1.php?passkey=$confirm_code</h2>
				<p>to reset password. This procedure would be valid for the next 5 minutes.</p>"; 
				$mail->AltBody="Your Confirmation link for the Association rules mining engine is\r\n{$_SERVER['SERVER_NAME']}/phpfunctions/forgot1.php?passkey=$confirm_code\r\nand it would be valid for the next 5 minutes.";
                //$message = "Please follow the link to reset your password. \r\n<a href="http://nireas.it.teithe.gr/WebApriori/phpfunctions/forgot1.php?passkey=$confirm_code"> ";                   
                //$mail->Body  = $message;
                if($mail->send()) {
					$message = "Your Reset password confirmation link has been sent to your email address ".$email.", and will be valid for the next 5 minutes.";
					echo "<script>alert('$message');
					window.location.href='../index.html';
					</script>";
				} else {
                    echo 'Email has not been sent for unknown reason';
                }
            }

        } else {
			http_response_code(400);
            echo "<script>alert('Internal server error');
			window.location.href='../index.html';</script>";
		}
	} else {
		http_response_code(403);
		echo "<script>alert('WebApriori. Access denied!!!');
		window.location.href='../index.html';</script>";
	}
?>

