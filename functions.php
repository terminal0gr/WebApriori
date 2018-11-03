<?php	
	function find_airline($airline_code)
	{
		$mysqli = new mysqli("127.0.0.1", "flightsuser", "flightsuser", "flightsdata");
		$query = "select airline from airlines where iata = ?";
	
		if ($stmt = $mysqli->prepare($query)) {

			/* bind parameters for markers */
			$stmt->bind_param("s", $airline_code);

			/* execute query */
			$stmt->execute();

			/* bind result variables */
			$stmt->bind_result($airline);

			/* fetch value */
			$stmt->fetch();

			

			/* close statement */
			$stmt->close();
		}

		/* close connection */
		$mysqli->close();

	
		return $airline;
	}
	
	function find_airport($airport_code)
	{
		$mysqli = new mysqli("127.0.0.1", "flightsuser", "flightsuser", "flightsdata");
		$query = "select city, country from airports where code = ?";
	
		if ($stmt = $mysqli->prepare($query)) {

			/* bind parameters for markers */
			$stmt->bind_param("s", $airport_code);

			/* execute query */
			$stmt->execute();

			/* bind result variables */
			$stmt->bind_result($city, $country);

			/* fetch value */
			$stmt->fetch();

			

			/* close statement */
			$stmt->close();
		}

		/* close connection */
		$mysqli->close();

		//$airport = ["city"->$city, "country"->$country];
		$airport = $city.",<br>".$country;
		return $airport;
		
		
		/*
		$airport_request = 'https://api.sandbox.amadeus.com/v1.2/airports/autocomplete?apikey=3jl39kYzxVtbQA9UWNg9BTV5Su3vLGnu&term='.$airport_code;
		$airport_response  = file_get_contents($airport_request);
		$airport_jsonobj  = json_decode($airport_response);
		
		foreach($airport_jsonobj as $airport_result)
		{
			if($airport_result->value == $airport_code) return $airport_result->label;
		}
		return $airport;*/
	}
	
	
	function getHttpCode($http_response_header)
	{
		if(is_array($http_response_header))
		{
			$parts=explode(' ',$http_response_header[0]);
			if(count($parts)>1) //HTTP/1.0 <code> <text>
				return intval($parts[1]); //Get code
		}
		return 0;
	}
	
	
?>