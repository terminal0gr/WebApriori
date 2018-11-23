<!DOCTYPE html>
<html lang="en">
<head>
  <title>Welcome to our Page</title>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
  <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
  <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>
</head>
<body>

<div class="container">
  
  <div id="myCarousel" class="carousel slide" data-ride="carousel">
    <!-- Indicators -->
    <ol class="carousel-indicators">
      <li data-target="#myCarousel" data-slide-to="0" class="active"></li>
      <li data-target="#myCarousel" data-slide-to="1"></li>
      <li data-target="#myCarousel" data-slide-to="2"></li>
      <li data-target="#myCarousel" data-slide-to="3"></li>
      <li data-target="#myCarousel" data-slide-to="4"></li>
    </ol>

    <!-- Wrapper for slides -->
    <div class="carousel-inner">
      <div class="item active">
        <img src="a1.jpg"  >
      </div>

      <div class="item">
        <img src="a2.jpg"  style="width:1200px;" style="height:1400px;">
      </div>
    
      <div class="item">
        <img src="a3.png" style="width:1200px;" style="height:1400px;">
      </div>
      <div class="item">
        <img src="a4.jpg"  style="width:1200px;" style="height:1400px;">
      </div>
      <div class="item">
        <img src="a5.jpg"  style="width:1200px;" style="height:1400px;">
      </div>
    </div>
    
    

    <!-- Left and right controls -->
    <a class="left carousel-control" href="#myCarousel" data-slide="prev">
      <span class="glyphicon glyphicon-chevron-left"></span>
      <span class="sr-only">Previous</span>
    </a>
    <a class="right carousel-control" href="#myCarousel" data-slide="next">
      <span class="glyphicon glyphicon-chevron-right"></span>
      <span class="sr-only">Next</span>
    </a>
  </div>
   

</div>
<!-- Division for Sign in And Register -->
<div class="container">
 
  <div class="panel-group" id="accordion">
    <div class="panel panel-default">
      <div class="panel-heading">
        <h4 class="panel-title">
          <a data-toggle="collapse" data-parent="#accordion" href="#collapse1">Sign In </a>
        </h4>
      </div>
      <div id="collapse1" class="panel-collapse collapse in">
        <form action="validation.php" method="post">
			<div >
				<label>email</label>
				<input type="email" name="email" class="form-control" placeholder="Email" required>
			</div>
			<div >
				<label>Password</label>
				<input type="password" name="password" class="form-control" required>
			</div>
			<button type="submit" class="btn btn-primary"> Login </button>
		</form>
      </div>
    </div>
    <div class="panel panel-default">
      <div class="panel-heading">
        <h4 class="panel-title">
          <a data-toggle="collapse" data-parent="#accordion" href="#collapse2">Register</a>
        </h4>
      </div>
      <div id="collapse2" class="panel-collapse collapse">
        <form action="resgistration.php" method="post">
			<div>
				<label>email</label>
				<input type="email" name="email" class="form-control" placeholder="Email" required>
			</div>
			<div>
				<label>Password</label>
				<input type="password" name="password" class="form-control" required>
			</div>
		
			<div>
				<label>Όνομα</label>
				<input type="name" name="name" class="form-control"  required>
			</div>
			<div>
				<label>Επίθετο</label>
				<input type="name" name="Fname" class="form-control" required>
			</div>
			<div>
				<p><img src="/captcha.php" width="120" height="30" border="1" alt="CAPTCHA"></p>
				<p><input type="text" size="6" maxlength="5" name="captcha" value=""><br>
				<small>copy the digits from the image into this box</small></p>	
			</div>
			<div>
				<button type="submit" class="btn btn-primary"> Register </button>
			</div>
		</div>		
    </div>
    
  </div> 
</div>
</body>
</html>
