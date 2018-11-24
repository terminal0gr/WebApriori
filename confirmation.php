<?php

 $con=mysqli_connect('localhost','flightsuser','flightsuser','flightsdata');

// Passkey that got from link
$passkey=$_GET['passkey'];

$temp_usertable="temp_members_db";

// Retrieve data from table where row that match this passkey
$sql1="SELECT * FROM $temp_usertable WHERE confirm_code ='$passkey'";
$result1=mysql_query($con,$sql1);

// If successfully queried
if($result1){

// Count how many row has this passkey
$count=mysql_num_rows($con,$result1);

// if found this passkey in our database, retrieve data from table "temp_members_db"
if($count==1){

$rows=mysql_fetch_array($result1);
$oname=$rows['oname'];
$email=$rows['email'];
$passwd=$rows['passwd'];
$fname=$rows['fname'];

$usertable="registered_members";

// Insert data that retrieves from "temp_members_db" into table "registered_members"
$sql2="INSERT INTO $usertable(oname, email, passwd, fname)VALUES('$oname', '$email', '$passwd', '$fname')";
$result2=mysql_query($con,$sql2);
}

// if not found passkey, display message "Wrong Confirmation code"
else {
echo "Wrong Confirmation code";
}

// if successfully moved data from table"temp_members_db" to table "registered_members" displays message "Your account has been activated" and don't forget to delete confirmation code from table "temp_members_db"
if($result2){

echo "Your account has been activated";

// Delete information of this user from table "temp_members_db" that has this passkey
$sql3="DELETE FROM $temp_usertable WHERE confirm_code = '$passkey'";
$result3=mysql_query($con,$sql3);

}

}
?>
