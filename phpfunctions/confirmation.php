<?php
include("config.php");

session_start();
    
$con = new mysqli(HOST, USERNAME, PWD, DB);

/* check connection */
if (mysqli_connect_errno()) {
	printf("<br>Connection error: %s\n", mysqli_connect_error());
	exit();
}

// Passkey that got from link
$passkey=$_GET['passkey'];

// Retrieve data from table where row that match this passkey
$sql1="SELECT * FROM temp_usertable WHERE confirm_code ='$passkey'";
$result1=mysqli_query($con,$sql1);

// If successfully queried
if($result1){
	// Count how many row has this passkey
	$count=mysqli_num_rows($result1);

	// if found this passkey in our database, retrieve data from table "temp_usertable"
	if($count==1){
		$rows=mysqli_fetch_array($result1);
		$oname=$rows['toname'];
		$email=$rows['temail'];
		$passwd=$rows['tpasswd'];
		$fname=$rows['tfname'];

		// Insert data that retrieves from "temp_usertable" into table "usertable"
		$sql2="INSERT INTO usertable(oname, email, passwd, fname)VALUES('$oname', '$email', '$passwd', '$fname')";
		$result2=mysqli_query($con,$sql2);
	} else { // if not found passkey, display message "Wrong Confirmation code"
		$message = "Wrong Confirmation code";
		echo "<script>alert('$message');
		window.location.href='../index.html';</script>";
	}

	// if successfully moved data from table"temp_members_db" to table "registered_members" displays message "Your account has been activated" and don't forget to delete confirmation code from table "temp_members_db"
	if($result2){
		$message = "Your account has been activated for the association rules mining engine. please Sign In with your credentials.";
		echo "<script>alert('$message');
		sessionStorage.setItem('SignIn',true);
		window.location.href='../index.html';</script>";

		// Delete information of this user from table "temp_members_db" that has this passkey
		$sql3="DELETE FROM temp_usertable WHERE confirm_code = '$passkey'";
		$result3=mysqli_query($con,$sql3);
	}
}

session_destroy();

?>
