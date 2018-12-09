<?php	
	function find_airline($airline_code)
	{
		$mysqli = new mysqli("127.0.0.1", "flightsuser", "flightsuser", "flightsdata");
		$query = "select airline from airlines where iata = ?";
	
		if ($stmt = $mysqli->prepare($query)) {
			$stmt->bind_param("s", $airline_code);
			$stmt->execute();
			$stmt->bind_result($airline);
			$stmt->fetch();

			$stmt->close();
		}

		$mysqli->close();
	
		return $airline;
	}
	
	function find_airport($airport_code)
	{
		$mysqli = new mysqli("127.0.0.1", "flightsuser", "flightsuser", "flightsdata");
		$query = "select city, country from airports where code = ?";
	
		if ($stmt = $mysqli->prepare($query)) {
			$stmt->bind_param("s", $airport_code);
			$stmt->execute();
			$stmt->bind_result($city, $country);
			$stmt->fetch();

			$stmt->close();
		}

		$mysqli->close();

		$airport = $city.",<br>".$country;
		return $airport;
	}
	
	
	function getHttpCode($http_response_header)
	{
		if(is_array($http_response_header))
		{
			$parts=explode(' ',$http_response_header[0]);
			if(count($parts)>1)
				return intval($parts[1]);
		}
		return 0;
	}
?>