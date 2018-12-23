<?php
	include("config.php");
	
	session_start();
	$con1 = new mysqli(HOST, USERNAME, PWD, DB);
	
	/* check connection */
	if ($con1->connect_error) {
		die("Connection Error" . $con1->connect_error);
	}
		
	/* Connection succesful*/
	$confirm_code=md5(uniqid(rand()));
	$email = mysqli_real_escape_string($con1, $_POST['email']);
	$query ="SELECT * FROM usertable WHERE email='$email'";
	$result = mysqli_query($con1,$query);
	$num=mysqli_num_rows($result);
	
	
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
	
	if(!$captcha_error) { 
        $sql="Select * from usertable
              where email='$email'";
		$result = mysqli_query($con1,$sql);
        
		if($result) {

            $message = "Your Confirmation link Has Been Sent To Your Email Address.".$email;
            echo "<script>alert('$message');
            window.location.href='../index.html';
            </script>";

            if($num==1) {

                $sql="INSERT INTO `temp_usertable` (`confirm_code`, `temail`, `tpasswd`, `toname`, `tfname`)
                     values ('$confirm_code', '$email' ,'','','')";
                $result = mysqli_query($con1,$sql);

                require_once("class.phpmailer.php");
                $mail = new PHPMailer;
                $mail -> IsSMTP();
                $mail->CharSet="UTF-8";       
                $mail->Host = 'smtp.teithe.gr';
                $mail->Port = 25;       
                $mail->From = 'ait242018@ait.teithe.gr';   
                $mail->FromName = 'Flights';
                $mail->addAddress($email);               
                $mail->Subject  = "Flights Scanner. Reset password";
                $message = "Please follow the link to reset your password. \r\nhttp://nireas.it.teithe.gr/webeng7/flights/phpfunctions/forgot1.php?passkey=$confirm_code ";                   
                $mail->Body  = $message;
                if(!$mail->send()) {
                    echo 'Email has not been sent.';
                    echo 'Error: ' . $mail->ErrorInfo;
                }
            }

        } else {
            header($_SERVER['SERVER_PROTOCOL'] . ' 500 Internal Server Error', true, 500);
            echo "<script>alert('Internal server error');
			window.location.href='../index.html';</script>";
		}
	} else {
		header($_SERVER['SERVER_PROTOCOL'] . ' 403 forbitten', true, 403);
		echo "<script>alert('Flight Scanner. Access denied!!!');
		window.location.href='../index.html';</script>";
	}
?>

