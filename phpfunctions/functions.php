<?php	

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