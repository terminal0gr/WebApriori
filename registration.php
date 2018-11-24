<?php
    $con=mysqli_connect('localhost','flightsuser','flightsuser','flightsdata');
    printf(mysqli_connect_error()); 
   $confirm_code=md5(uniqid(rand()));
   
   $email = mysqli_real_escape_string($con, $_POST['email']);
  $passwd = mysqli_real_escape_string($con, $_POST['passwd']);
  $oname = mysqli_real_escape_string($con, $_POST['oname']);
  $fname = mysqli_real_escape_string($con, $_POST['fname']);
   $s="SELECT * FROM usertable WHERE email='$email'";
   $result = mysqli_query($con,$s);
	$num=mysqli_num_rows($result);
   if($num==1){
	   echo"To email υπάρχει ήδη";
	}else{
		
		$sql="INSERT INTO temp_usertable(confirm_code,temail,tpasswd,tname,tfname)VALUES('$confirm_code','$email','$passwd','$oname','$fname')";
		$result = mysqli_query($con,$sql);
		if($result){

			$to=$email;
			$subject="Your confirmation link here";
			$header="from: nasia sklavou <slvnasia@gmail.com>";
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
   
?>
