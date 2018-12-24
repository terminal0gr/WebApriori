<?php
	include("config.php");
	include("jwt_helper.php");
	session_start(); 
    
	if ($_SERVER["REQUEST_METHOD"] == "POST") {

		$con = new mysqli(HOST, USERNAME, PWD, DB);
		//$con = mysqli_connect("localhost", "webeng7", "webeng71819", "webeng7");
	
		/* check connection */
		if (mysqli_connect_errno()) {
			printf("<BR>Fatal Error: %s\n", mysqli_connect_error());
			exit();
		}

        //The FILTER_SANITIZE_EMAIL filter removes all illegal characters from an email address
        $email = filter_var(trim($_POST["email"]), FILTER_SANITIZE_EMAIL);
        //mysqli_real_escape_string function is used to create a legal SQL string that you can use in an SQL statement.
		$email = mysqli_real_escape_string($con, $_POST['email']);
		$passwd = mysqli_real_escape_string($con, $_POST['passwd']);
        
        if ( empty($email) OR empty($passwd) OR !filter_var($email, FILTER_VALIDATE_EMAIL)) {
            // Set a 400 (bad request) response code and exit.
            http_response_code(400);
            echo "There was a problem with your email and/or password. Please correct the form and try again.";
            exit;
        }
    
        $passwd=md5($passwd);
		$s="SELECT * FROM usertable WHERE email='$email' and passwd='$passwd'";
		$result = mysqli_query($con,$s);
		$num=mysqli_num_rows($result);

		// If result matched $myusername and $mypassword, table row must be 1 row
		if($num==1){

            $rowobj = $result->fetch_object();

			$token = array();
			$token['id'] = $email;
			$key=SERVERKEY.date("m.d.y");

			http_response_code(200);
            $JsonReq = array('http_response_code' => 200, 'token' => JWT::encode($email, $key), 'apikey' => apikey, 'name' => $rowobj->fname." ".$rowobj->oname, 'message' => 'success');
            print json_encode($JsonReq);

		} else {
			//set a 403 (forbidden) response code.	
			http_response_code(403);
			echo "403 Username and/or Password incorrect.\nPlease try again.";

		}

	} else {
		// Not a POST request, set a 403 (forbidden) response code.
		http_response_code(403);
		echo "There was a problem with your submission, please try again.";
	}
?>

