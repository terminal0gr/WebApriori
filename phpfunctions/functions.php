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
	};

	function generateRandomString($length = 10) {
        $characters = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ';
        $charactersLength = strlen($characters);
        $randomString = '';
        for ($i = 0; $i < $length; $i++) {
            $randomString .= $characters[rand(0, $charactersLength - 1)];
        }
        return $randomString;
	};
	
	function deleteDir($dir) {
		try {
			if (file_exists($dir)) {
				$it = new RecursiveDirectoryIterator($dir, RecursiveDirectoryIterator::SKIP_DOTS);
				$files = new RecursiveIteratorIterator($it,
							RecursiveIteratorIterator::CHILD_FIRST);
				foreach($files as $file) {
					if ($file->isDir()){
						rmdir($file->getRealPath());
					} else {
						unlink($file->getRealPath());
					}
				}
				rmdir($dir);
			}
			return true;
		} catch (Exception $e) {  
			print($e);
			return false;
		};	
	};

	function execInBackground($cmd) {
		if (substr(php_uname(), 0, 7) == "Windows"){
			pclose(popen("start /B ". $cmd, "r")); 
		}
		else {
			exec($cmd . " > /dev/null &");  
		}
	} 

?>