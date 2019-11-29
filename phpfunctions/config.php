<?php
    //MariaDB/Mysql settings
	//define( 'USERNAME', 'webeng7' );
	//define( 'PWD', 'webeng71819' );   
	//define( 'DB', 'webeng7' );   
	define( 'USERNAME', 'aprioriUser' );
	define( 'PWD', 'aprioripwd' );   
	define( 'DB', 'aprioriBase' );   
	define( 'HOST', 'localhost' ); 
	define( 'SERVERKEY', 'e486n8wn76v7n69v7as678z7n674b7zx7vb7' ); 

	//////////////////////////////////////////////
	//Site settings
	define('siteRoot','http://localhost/webapriori/');


	//////////////////////////////////////////////
	//SMTP Settings

	//$mail->Host = 'smtp.teithe.gr';
	//$mail->Port = 25; 

	// $mail->Host = 'smtp.mail.yahoo.com';
	// $mail->Port = 465; 
	// $mail->SMTPAuth = true;                 // Enable SMTP authentication
	// $mail->Username = 'terminal_gr@yahoo.com';  // SMTP username
	// $mail->Password = 'samall321&@!';    // SMTP password
	// $mail->SMTPSecure = 'ssl'; 

	define('smtpHost','smtp.office365.com');
	define('smtpPort',587);
	define('smtpAuth',true);
	define('smtpUsername','malliaridis@mentor.com.gr');
	define('smtpPassword','sakhs13!');
	define('smtpSecure','tls');
	define('smtpFrom','malliaridis@mentor.com.gr');	
	define('smtpFromName','Association rules mining engine');		

?>