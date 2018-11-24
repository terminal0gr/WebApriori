<?php
   session_start();
  
 
 $con=mysqli_connect('localhost','flightsuser','flightsuser','flightsdata');
   printf(mysqli_connect_error());
   
   $email = mysqli_real_escape_string($con, $_POST['email']);
  $passwd = mysqli_real_escape_string($con, $_POST['passwd']);
 
   $s="SELECT * FROM usertable WHERE email='$email'&& passwd=md5('$passwd')";
   $result = mysqli_query($con,$s);
   $num=mysqli_num_rows($result);
   if($num==1){
	   header('location:search.php');
	}else{
		header('location:index.php');
		
	}
?>

