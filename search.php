<?php
	
	include("./config.php");
	include("./functions.php");


	$mysqli = new mysqli(HOST, USERNAME, PWD, DB);
	/* check connection */
	if (mysqli_connect_errno()) {
		printf("<BR>Αποτυχία Σύνδεσης: %s\n", mysqli_connect_error());
		exit();
	}
    
    ini_set("allow_url_fopen", 1); 
    
	
?>

<!DOCTYPE html>
<head>
	<meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    
    <!-- Bootstrap CSS -->
	<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css" integrity="sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO" crossorigin="anonymous">

    <link rel="icon" type="image/png" href="./images/plane_02.png"/>
    

    <link rel="stylesheet" href="./styles.css" type="text/css" />

	<script src="http://code.jquery.com/jquery-3.3.1.js"></script>
	<script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.3/umd/popper.min.js" integrity="sha384-ZMP7rVo3mIykV+2+9J3UJ46jBk0WLaUAdn689aCwoqbBJiSnjAK/l8WvCWPIPm49" crossorigin="anonymous"></script>
	<script src="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/js/bootstrap.min.js" integrity="sha384-ChfqqxuZUCnJSK3+MXmPNIyE6ZbWh2IMqE241rYiqJxyMiZ6OW/JmZQ5stwEULTy" crossorigin="anonymous"></script>

	<link rel="stylesheet" href="//code.jquery.com/ui/1.12.1/themes/base/jquery-ui.css">
	<script src="http://code.jquery.com/ui/1.12.1/jquery-ui.js"></script>
	<script src="scripts/scripts.js"></script>
	

    <title>Flight Scanner</title>

	<script>
		$( window ).resize(function() {
			if ($(window).width() <= 768 || $(window).height() <= 576) {
				$('#c-footer').removeClass('fixed-bottom');
			}
			else {
				$('#c-footer').addClass('fixed-bottom')
			}
		});

		$(function() {

			$('#navbar-brand').html('Flight scanner ' +  sessionStorage.getItem('version'));

			var dateFormat = "dd/mm/yy",
				departure_date = $("#departure_date")
					.datepicker({
						dateFormat: "dd/mm/yy",
						showAnim: "blind",
						showButtonPanel: true,
						minDate: 0
					})
					.on( "change", function() {
						return_date.datepicker( "option", "minDate", getDate( this ) );
						$('#ddate').val( $.datepicker.formatDate( 'yy-mm-dd', new Date( getDate( this ) ) ) );
					}),
				return_date = $("#return_date")
					.datepicker({
						dateFormat: "dd/mm/yy",
						showAnim: "blind",
						showButtonPanel: true,
						minDate: 0,
						closeText: 'Clear',
						onClose: function () {
							var event = arguments.callee.caller.caller.arguments[0];                
							if ($(event.delegateTarget).hasClass('ui-datepicker-close')) {
								$(this).val('');
							}
						}
					})
					.on( {  change: function() {
								departure_date.datepicker( "option", "maxDate", getDate( this ) );
								$('#rdate').val( $.datepicker.formatDate( 'yy-mm-dd', new Date( getDate( this ) ) ) );
							},
							close: function () {
								var event = arguments.callee.caller.caller.arguments[0];                
								if ($(event.delegateTarget).hasClass('ui-datepicker-close')) {
									$(this).val('');
								}
							}
					} );
			
			
			function getDate( element ) {
			  var date;
			  try {
				date = $.datepicker.parseDate( dateFormat, element.value );
			  } catch( error ) {
				date = null;
			  }
		 
			  return date;
			}
			
			$( "#dialog" ).dialog({ autoOpen: false });
			$( "#opener" ).click(function() {
				$( "#dialog" ).dialog( "open" );
			});
			
			function log( message ) {
				$( "<div>" ).text( message ).prependTo( "#log" );
				$( "#log" ).scrollTop( 0 );
			}
			
			$( "#origin_descr" ).autocomplete({
				source: function( request, response ) {
					$.ajax({
						url: "https://api.sandbox.amadeus.com/v1.2/airports/autocomplete",
						dataType: "json",
						data: {
							apikey: "djnSPkH5LeLwOsA8gbApHjGjdCkaRpAa",
							term: request.term
						},
						success: function( data ) {
							response( data );
						}
					});
				},
				minLength: 3,
				select: function(event, ui) {
					event.preventDefault();
					$("#origin_descr").val(ui.item.label);
					$("#origin").val(ui.item.value);
				},
				focus: function(event, ui) {
					event.preventDefault();
					$("#origin_descr").val(ui.item.label);
				},
				open: function() {
					$( this ).removeClass( "ui-corner-all" ).addClass( "ui-corner-top" );
				},
				close: function() {
					$( this ).removeClass( "ui-corner-top" ).addClass( "ui-corner-all" );
				}
			});
			
			$( "#destination_descr" ).autocomplete({
				source: function( request, response ) {
					$.ajax({
						url: "https://api.sandbox.amadeus.com/v1.2/airports/autocomplete",
						dataType: "json",
						data: {
							apikey: "djnSPkH5LeLwOsA8gbApHjGjdCkaRpAa",
							term: request.term
						},
						success: function( data ) {
							response( data );
						}
					});
				},
				minLength: 3,
				select: function(event, ui) {
					event.preventDefault();
					$("#destination_descr").val(ui.item.label);
					$("#destination").val(ui.item.value);
				},
				focus: function(event, ui) {
					event.preventDefault();
					$("#destination_descr").val(ui.item.label);
				},
				open: function() {
					$( this ).removeClass( "ui-corner-all" ).addClass( "ui-corner-top" );
				},
				close: function() {
					$( this ).removeClass( "ui-corner-top" ).addClass( "ui-corner-all" );
				}
			});			
		
		
			$( "#error-dialog" ).dialog({
				autoOpen: false,
				modal: true,
				buttons: {
					Ok: function() {
						$( this ).dialog( "close" );
					}
				}
			});
		
		
			$( "form" ).submit(function( event ) {
				var flist = "";
				
				if ( $( "#origin" ).val() === "" ) { flist += "<li>Αναχώρηση από</li>"; }
				if ( $( "#destination" ).val() === "" ) { flist += "<li>Άφιξη σε</li>"; }
				if ( $( "#ddate" ).val() === "" ) { flist += "<li>Ημ/νία Αναχώρησης</li>"; }

				var direction = $('input[name=direction]:checked').val();
				if ( direction === "2" ) { 
					if ( $( "#rdate" ).val() === "" ) { 
						flist += "<li>Ημ/νία Άφιξης</li>"; 
					}
				}
				
				if (flist === "") {

					var Mdata = "apikey=djnSPkH5LeLwOsA8gbApHjGjdCkaRpAa";
					Mdata += "&number_of_results=250";
					Mdata += "&currency=EUR";
					Mdata += "&origin=" + $("#origin").val();
					Mdata += "&destination=" + $("#destination").val();
					Mdata += "&departure_date=" + $("#ddate").val();
					if (direction === "2") {
						Mdata += "&return_date=" + $("#rdate").val();
					}

					$( "#searching" ).show();
					$( "#apidiv" ).html( "Retrieval start...." );
					/*********************************************/

					$.ajax({
						url: "https://api.sandbox.amadeus.com/v1.2/flights/low-fare-search",
						dataType: "json",
                        data: Mdata,
						success: function(response) {

							$("#apidiv").html(FillTheTable(response));

						} 
                    }).fail(function (jqXHR, textStatus, errorThrown) {
                        alert(textStatus+": "+errorThrown+"\n\n"+to_s(jqXHR.responseText));
                        $(e.target).prop('disabled', false);
                    });
					
					/*********************************************/
					
					$( "#searching" ).hide();
					
					event.preventDefault();
					
					return;
				} else {
					$( "#error-dialog" ).html( "<p><span class='ui-icon ui-icon-alert' style='float:left; margin:0 7px 50px 0;'></span>Δεν έχετε συμπληρώσει όλα τα υποχρεωτικά πεδία:</p><p><ul>" + flist + "</ul></p>" );
					$( "#error-dialog" ).dialog( "open" );

					event.preventDefault();
				}
			});
			
			$( "#searching" ).hide();
		
		});

		function showRequest() {
			var x = document.getElementById("apirequest");
			var b = document.getElementById("brequest");
			
			if (x.style.display === "none") {
				x.style.display = "block";
				b.innerHTML = "Hide Request";
			} else {
				x.style.display = "none";
				b.innerHTML = "Show Request";
			}
		}
	
		function waydirection(choice) {
			var returnDate = document.getElementById("return_date");
			
			if (choice === 1) {
				returnDate.type = "hidden";
				returnDate.value = "";
			} else {
				returnDate.type = "text";
			}
		}
		
	</script>

</head>

<body>

	<nav class="navbar navbar-expand-sm navbar-dark bg-dark">
		<a id="navbar-brand" class="navbar-brand" href="#">Flight scanner     </a>
		<ul class="navbar-nav mr-auto">
			<li class="nav-item">
				<a class="nav-link" href="index.php">Αρχική</a>
			</li>
			<li class="nav-item">
				<a class="nav-link active">Αναζήτηση</a>
			</li>
		</ul>
		<ul class="navbar-nav ml-auto">
			<li class="nav-item">
				<a class="nav-link" href = "logout.php">Έξοδος</a>
			</li>
		</ul>
	</nav>

	<div class="container">
   
        <!-- <div class="float-right"><button class="btn btn-secondary btn-sm" type="button" id='brequest' onclick="showRequest()">Show Request</button></div> -->
		
		<form method="post" action="">

			<br>
            <div class="border border-primary rounded">
				<table >
				<tr><td colspan=3>
					<!-- <div class="form-group"> -->
						<label >Απλή μετάβαση
							<input type="radio" id="direction" name="direction" value=1 onclick="waydirection(1)" <?php
								if (isset($_POST['direction'])){
									if($_POST['direction']==1) echo("checked");
								} else { 
									echo("checked");
								}
								?>> 
						</label>
						<label >Με επιστροφή
							<input type="radio" id="direction" name="direction" value=2 onclick="waydirection(2)" <?php
								if (isset($_POST['direction'])){
									if($_POST['direction']==2) echo("checked");
								}
								?>>
							<span class="checkmark"></span>
						</label>
					<!-- </div> -->
				</td></tr>
				<tr><td>
					<input type="text" id="origin_descr" name="origin_descr" placeholder="Αναχώρηση από ..." class="form-control" value="<?php 
						if (isset($_POST['origin_descr'])){
							echo($_POST['origin_descr']); }
						else { 
							echo('');
						}
					?>"/>
				</td><td>
					<input type="text" id="departure_date"  name="departure_date" size=8 placeholder="Αναχώρηση" autocomplete="off"  class="form-date form-control" value="<?php 
						if (isset($_POST['departure_date'])){
							echo($_POST['departure_date']); 
						} else {
							echo("");
						}
					?>"/>
				</td><td rowspan=3>
					<input type="submit" value="Αναζήτηση" name="submit" class="btn btn-primary" id="searchButton" />
				</td></tr>
				<tr><td>
					<input type="text" id="destination_descr"  name="destination_descr" placeholder="Άφιξη σε ..." class="form-control" value="<?php 
						if (isset($_POST['destination_descr'])){
							echo($_POST['destination_descr']); }
						else { 
							echo('');
						}
					?>"/>
				</td><td>
				<!--<label class="control-label">Ημ/νία επιστροφής: </label>-->
				<input type="<?php 
					if (isset($_POST['direction'])){
						if($_POST['direction']==2) {
							echo("text");
						} else {
							echo("hidden");
						}
					} else {
						echo("hidden");
					}?>" id="return_date" name="return_date" size=7 placeholder="Επιστροφή" autocomplete="off"  class="form-control form-date" value="<?php 
					if (isset($_POST['return_date'])){
						echo($_POST['return_date']); }
					else { 
						echo('');
					}
					?>"/>
				</td></tr>
				
				</table>
			</div>

			<input type="hidden" id="ddate"  name="ddate" size=6 placeholder="Αναχώρηση" autocomplete="off"  class="form-date form-control"> 
			<input type="hidden" id="rdate"  name="rdate" size=6 placeholder="Άφιξη" autocomplete="off"  class="form-date form-control"> 
				
			<input type="hidden" id="origin" name="origin" value="<?php 
				if (isset($_POST['origin'])){
					echo($_POST['origin']); }
				else { 
					echo('');
				}
				?>"/>
			<input type="hidden" id="destination" name="destination" value="<?php 
				if (isset($_POST['destination'])){
					echo($_POST['destination']); }
				else { 
					echo('');
				}
				?>"/>
		</form>


	<div id="error-dialog" title="Έλεγχος πεδίων"></div>
	<div id="result-dialog" title="Αποτελέσματα αναζήτησης"></div>
	<div id="searching" class="center-div"></div>
	<div id="apidiv"></div>
	
	</div>

	<br>
	<br>

    <footer>
		<nav id="c-footer" class="navbar fixed-bottom navbar-expand-md navbar-dark bg-dark">
			<span class="navbar-text ">Εφαρμογή αναζήτησης πτήσεων χαμηλού κόστους &middot; Π.Μ.Σ. Ευφυείς Τεχνολογίες Διαδικτύου &copy; 2018-2019</span>
		</nav>
	</footer>


	<?php /*
		if (isset($_POST['submit'])) {
			
			$tdeparture_date = ((strpos($_POST["departure_date"], "-") === true ) ? explode("-", $_POST["departure_date"]) : explode("/", $_POST["departure_date"]) );
			$fdeparture_date = $tdeparture_date[2]."-".$tdeparture_date[1]."-".$tdeparture_date[0];
			
			$request = 'https://api.sandbox.amadeus.com/v1.2/flights/low-fare-search?apikey=djnSPkH5LeLwOsA8gbApHjGjdCkaRpAa&currency=EUR&origin='.$_POST["origin"].'&number_of_results=250'.'&destination='.$_POST["destination"].'&departure_date='.$fdeparture_date;

 			if ($_POST["return_date"]!="") {
				$treturn_date = ((strpos($_POST["return_date"], "-") === true ) ? explode("-", $_POST["return_date"]) : explode("/", $_POST["return_date"]));
				$freturn_date = $treturn_date[2]."-".$treturn_date[1]."-".$treturn_date[0];
				$request .= '&return_date='.$freturn_date;
			}
			
			echo "<div id='apirequest' style='display:none;'>Request url: <br><a target='_BLANK' href='".htmlentities($request)."'>".htmlentities($request)."</a></b></div><br>";
			$response = @file_get_contents($request);
			$code = getHttpCode($http_response_header);
			$jsonobj = json_decode($response);

			echo "<br><div id='flightsnum'><u>ΑΠΟΤΕΛΕΣΜΑΤΑ ΑΝΑΖΗΤΗΣΗΣ:</u></div><br>";
			
			if($code == 400) {
				echo "Δεν βρέθηκαν πτήσεις με τα κριτήρια που δώσατε!";
			} elseif ($code == 200) {
				$flights_sum = 0;
				
				echo('<table id="results" border=1>');
				?>
				<tr>
				    <th rowspan=2>Διάρκεια</th>
					<th colspan=2>Αναχώρηση</th>
					<th colspan=2>Άφιξη</th>
					<th colspan=3>Πτήση</th>
					<th colspan=2 rowspan=2 >Θέση</th>
					<th rowspan=2>Διαθέσιμες<br>θέσεις</th>
					<th colspan=3>Συν. Κόστος</th>
				</tr>
				<tr>
				    <th>Αεροδρόμιο</th>
					<th>Ώρα</th>
					<th>Αεροδρόμιο</th>
					<th>Ώρα</th>
					<th>Airline</th>
					<th>Αριθμός</th>
					<th>Αεροσκάφος</th>
					<th>Total Price</th>
					<th>Total Fare</th>
					<th>Tax</th>
				</tr>
				
				<?php
				foreach($jsonobj->results as $results)
				{
					echo('<tr>');
					
					foreach($results->itineraries as $itineraries) {
						$dromologia=count($itineraries->outbound->flights);
						$duration = explode(":", $itineraries->outbound->duration);
						
						$totallines=$dromologia;
                        If(isset($itineraries->inbound)) {
							$totallines+=count($itineraries->inbound->flights);
						}	
						
						$flights_sum++;
						echo("<td align=center rowspan=".$dromologia."><b>Μετάβαση</b><br>".$duration[0]."ώ ".$duration[1]."λ<br>");
						
						if($dromologia == 1) 
							echo("<b>Απευθείας πτήση</b></td>");
						else
							echo("<b>".($dromologia - 1).(($dromologia - 1)>1?" στάσεις":" στάση")."</b></td>");
						
						$index=0;
						
						foreach($itineraries->outbound->flights as $flights) {

							if($index > 0) echo("<tr>");
														
							echo("<td align=center>".$flights->origin->airport."<br>".find_airport($flights->origin->airport)."</td>");
							
							$departure=explode("T", $flights->departs_at);
							$tmp_departure_date = explode("-", $departure[0]);
							$departure_date = $tmp_departure_date[2]."/".$tmp_departure_date[1]."/".$tmp_departure_date[0];
							$departure_time = $departure[1];
							echo("<td align=center>".$departure_date."<br>".$departure_time."</td>");
							
							echo("<td align=center>".$flights->destination->airport."<br>".find_airport($flights->destination->airport)."</td>");
							
							$arrival=explode("T", $flights->arrives_at);
							$tmp_arrival_date = explode("-", $arrival[0]);
							$arrival_date = $tmp_arrival_date[2]."/".$tmp_arrival_date[1]."/".$tmp_arrival_date[0];
							$arrival_time = $arrival[1];
							echo("<td align=center>".$arrival_date."<br>".$arrival_time."</td>");
							
							echo("<td align=center>".$flights->operating_airline."<br>".find_airline($flights->operating_airline)."</td>");
							echo("<td align=center>".$flights->flight_number."</td>");
							echo("<td align=center>".$flights->aircraft."</td>");
							echo("<td align=center>".$flights->booking_info->travel_class."</td>");
							echo("<td align=center>".$flights->booking_info->booking_code."</td>");
							$seats=$flights->booking_info->seats_remaining;
							if($flights->booking_info->seats_remaining==9) $seats=">=9";
							echo("<td align=center>".$seats."</td>");

							if($index == 0) echo("<td align=center rowspan=".$totallines.">".$results->fare->total_price."</td>");
							if($index == 0) echo("<td align=center rowspan=".$totallines.">".$results->fare->price_per_adult->total_fare."</td>");
							if($index == 0) echo("<td align=center rowspan=".$totallines.">".$results->fare->price_per_adult->tax."</td>");

							echo("</tr>");
							
							$index++;
						}
						
						If(isset($itineraries->inbound)) {

							$dromologia=count($itineraries->inbound->flights);
							$duration = explode(":", $itineraries->inbound->duration);
							
							echo("<td align=center rowspan=".$dromologia."><b>Επιστροφή</b><br>".$duration[0]."ώ ".$duration[1]."λ<br>");
							if($dromologia == 1) 
								echo("<b>Απευθείας πτήση</b></td>");
							else
								echo("<b>".($dromologia - 1).(($dromologia - 1)>1?" στάσεις":" στάση")."</b></td>");
							
							$index=0;

							foreach($itineraries->inbound->flights as $flights) {
								if($index > 0) echo("<tr>");
								
								echo("<td align=center>".$flights->origin->airport."<br>".find_airport($flights->origin->airport)."</td>");
								
								$departure=explode("T", $flights->departs_at);
								$tmp_departure_date = explode("-", $departure[0]);
								$departure_date = $tmp_departure_date[2]."/".$tmp_departure_date[1]."/".$tmp_departure_date[0];
								$departure_time = $departure[1];
								echo("<td align=center>".$departure_date."<br>".$departure_time."</td>");
								
								echo("<td align=center>".$flights->destination->airport."<br>".find_airport($flights->destination->airport)."</td>");
								
								$arrival=explode("T", $flights->arrives_at);
								$tmp_arrival_date = explode("-", $arrival[0]);
								$arrival_date = $tmp_arrival_date[2]."/".$tmp_arrival_date[1]."/".$tmp_arrival_date[0];
								$arrival_time = $arrival[1];
								echo("<td align=center>".$arrival_date."<br>".$arrival_time."</td>");
								
								echo("<td align=center>".$flights->operating_airline."<br>".find_airline($flights->operating_airline)."</td>");
								echo("<td align=center>".$flights->flight_number."</td>");
								echo("<td align=center>".$flights->aircraft."</td>");
								echo("<td align=center>".$flights->booking_info->travel_class."</td>");
								echo("<td align=center>".$flights->booking_info->booking_code."</td>");

								$seats=$flights->booking_info->seats_remaining;
								if($flights->booking_info->seats_remaining==9) $seats=">=9";
								echo("<td align=center>".$seats."</td>");
								
								echo("</tr>");

								$index++;
							}
						}
						
						echo('<tr><td colspan=14 style="background: lightblue; line-height:0.01;">&nbsp;</td></tr>');						
					}
				}
				echo('</table>');
				
				echo '<script>
							var numobj = document.getElementById("flightsnum");
							numobj.innerHTML = "<u>ΑΠΟΤΕΛΕΣΜΑΤΑ ΑΝΑΖΗΤΗΣΗΣ:</u> <b>(Βρέθηκαν " + '.$flights_sum.' + " πτήσεις)</b>";
							
							$( "#result-dialog" ).dialog({
								autoOpen: false,
								modal: true,
								buttons: {
									Ok: function() {
										$( this ).dialog( "close" );
									}
								}
							});
				
							$( "#result-dialog" ).html( "<p><span class=\'ui-icon ui-icon-search\' style=\'float:left; margin:0 7px 50px 0;\'></span>Βρέθηκαν <b>'.$flights_sum.'</b> πτήσεις με τα κριτήρια που δώσατε</p><p></p>" );
							$( "#result-dialog" ).dialog( "open" );
					   </script>';
				
			}	
		} else {
			unset($_POST);
			$_POST = array();
		} */
		?>
	

</body>
</html>
