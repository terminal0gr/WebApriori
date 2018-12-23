<?php
    $passkey = $_GET['passkey'];
    include("config.php");
    $con1 = new mysqli(HOST, USERNAME, PWD, DB);
    /* check connection */
    if ($con1->connect_error) {
        die("Connection Error" . $con1->connect_error);
    }
    $query ="SELECT * FROM temp_usertable WHERE confirm_code='$passkey'";
	$result = mysqli_query($con1,$query);
    $num=mysqli_num_rows($result);
    if ($num ==1){
?>
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css" integrity="sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO" crossorigin="anonymous">

    <link rel="icon" type="image/png" href="./images/plane_02.png"/>
  
    <link rel="stylesheet" href="css/styles.css" type="text/css" />
  
    <script src="http://code.jquery.com/jquery-3.3.1.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.3/umd/popper.min.js" integrity="sha384-ZMP7rVo3mIykV+2+9J3UJ46jBk0WLaUAdn689aCwoqbBJiSnjAK/l8WvCWPIPm49" crossorigin="anonymous"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/js/bootstrap.min.js" integrity="sha384-ChfqqxuZUCnJSK3+MXmPNIyE6ZbWh2IMqE241rYiqJxyMiZ6OW/JmZQ5stwEULTy" crossorigin="anonymous"></script>

    <title>Flight Scanner</title>

	<script>
    	$(function() {
            M_F();
        });

        function M_F() {
            if ($(window).width() <= 800 || $(window).height() <= 600) {
                $('#c-footer').removeClass('fixed-bottom');
            }
            else {
                $('#c-footer').addClass('fixed-bottom')
            }
        }

        $( window ).resize(function() {
            M_F();
        });

		function CheckVer(){
			var t= document.getElementById("passwd" );
			var t2= document.getElementById("vpasswd");
			if(t && t2){
				if(t.value !== t2.value){
					alert('Passwords do not match!');
					t.focus();
					return false;
				}
				return true;
			}
		}
	</script>

</head>

<body>

    <nav class="navbar navbar-expand-sm navbar-dark bg-dark">
		<a id="navbar-brand" class="navbar-brand d-none d-sm-block" href="#">Flight scanner     </a>
	</nav>

    <br>
    <br>

	<div class="mx-auto border rounded mb-3 p-2" style="width: 329px;" >
		<h4 class="text-center">Reset you password</h4>
		<form id="ajax-contact" action= "forgot2.php" method="post">
			<div class="p-1">
				<label for="passwd">Enter your new password.</label>
				<input type="password" id="passwd" name="passwd" class="form-control" pattern="(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}" title="It must contain at least one number, a capital and a lower case and consist of at least 8 characters "  required>
			</div>
			<div class="p-1">
				<label for="vpasswd">Verify your new password.</label>
				<input id="vpasswd" type="password" name="vpasswd" onblur="CheckVer()" class="form-control" pattern="(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}"title="It must contain at least one number, a capital and a lower case and consist of at least 8 characters "  required>
            </div>

            <input id="passkey" type="hidden" name="passkey" class="form-control" value="<?php echo $passkey;?>" > 
           
			<div class=" p-1" >
				<button type="submit" class="btn btn-primary btn-block mt-3" >Send password reset email</button>
            </div>
		</form>
	</div>

    <footer>
        <nav id="c-footer" class="navbar fixed-bottom navbar-expand-lg navbar-dark bg-dark">
        	<span class="navbar-text ">Low fare flights search engine &middot; MSc in Web Intelligence &copy; 2018-2019</span>
        </nav>
	</footer>

</body>
</html>
<?php
    } else{
        header("Location: http://nireas.it.teithe.gr/webeng7/flights/index.html");
    }
?>