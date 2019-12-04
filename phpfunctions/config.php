<?php 
    //Msqli Settings
	define( 'USERNAME', 'aprioriUser' );
	define( 'PWD', 'aprioripwd' );   
	define( 'DB', 'aprioriBase' );   
	define( 'HOST', 'localhost' ); 

	//Site settings
	define( 'SERVERKEY', 'e486n8wn76v7n69v7as678z7n674b7zx7vb7' ); 
	define('siteRoot','https://nireas.it.teithe.gr/webapriori/');
	define('MaxDatasets', 10);
	
	//SMTP Settings
	//$mail->Host = 'smtp.teithe.gr';
	//$mail->Port = 25; 
	// define('smtpHost','smtp.office365.com');
	// define('smtpPort',587);

	define('smtpHost','smtp.office365.com');
	define('smtpPort',587);
	define('smtpAuth',true);
	define('smtpUsername','malliaridis@mentor.com.gr');
	define('smtpPassword','sakhs13!');
	define('smtpSecure','tls');
	define('smtpFrom','malliaridis@mentor.com.gr');	
	define('smtpFromName','Association rules mining engine');		

?>