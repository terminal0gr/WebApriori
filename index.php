<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    
    <!-- Bootstrap CSS -->
	  <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css" integrity="sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO" crossorigin="anonymous">
    <!-- <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css"> -->

    <link rel="icon" type="image/png" href="./images/plane_02.png"/>
    
  
    <link rel="stylesheet" href="./styles.css" type="text/css" />
  

    <script src="http://code.jquery.com/jquery-3.3.1.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.3/umd/popper.min.js" integrity="sha384-ZMP7rVo3mIykV+2+9J3UJ46jBk0WLaUAdn689aCwoqbBJiSnjAK/l8WvCWPIPm49" crossorigin="anonymous"></script>

    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/js/bootstrap.min.js" integrity="sha384-ChfqqxuZUCnJSK3+MXmPNIyE6ZbWh2IMqE241rYiqJxyMiZ6OW/JmZQ5stwEULTy" crossorigin="anonymous"></script>
    <!-- <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script> -->


    <title>Flight Scanner V1.1</title>

</head>

<body>


	<nav class="navbar navbar-expand-sm navbar-dark bg-dark">
		<a class="navbar-brand" href="#">Flight scanner 1.1</a>
		<ul class="navbar-nav mr-auto">
			<li class="nav-item">
				<a class="nav-link active">Αρχική</a>
			</li>
			<li class="nav-item">
				<a class="nav-link" href="search.php">Αναζήτηση</a>
			</li>
		</ul>
		<ul class="navbar-nav ml-auto">
			<li class="nav-item">
				<a class="nav-link">Εγγραφή</a>
			</li>
			<li class="nav-item">
				<a class="nav-link">Είσοδος</a>
			</li>
			<li class="nav-item">
				<a class="nav-link">Έξοδος</a>
			</li>
		</ul>
	</nav>

    <br>


	<div class="container-fluid">
  
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
        <img src="images/a1.jpg" style="width:800px;" style="height:600px;"> >
      </div>
      <div class="item">
        <img src="images/a2.jpg" style="width:800px;" style="height:600px;"> >
      </div>
      <div class="item">
        <img src="images/a3.png" style="width:800px;" style="height:600px;"> >
      </div>
      <div class="item">
        <img src="images/a4.jpg" style="width:800px;" style="height:600px;"> >
      </div>
      <div class="item">
        <img src="images/a5.jpg" style="width:800px;" style="height:600px;"> >
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

    <br>
    <br>
    <br>

    <footer>
	<nav class="navbar fixed-bottom navbar-expand-lg navbar-dark bg-dark">
		<span class="navbar-text ">Εφαρμογή αναζήτησης πτήσεων χαμηλού κόστους &middot; Π.Μ.Σ. Ευφυείς Τεχνολογίες Διαδικτύου &copy; 2018-2019</span>
	</nav>
	</footer>


</body>
</html>
