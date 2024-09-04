<?php
    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, "http://localhost:8080/run-script");
    curl_setopt($ch, CURLOPT_POST, 1);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    $response = curl_exec($ch);
    curl_close($ch);

    echo $response;

?>