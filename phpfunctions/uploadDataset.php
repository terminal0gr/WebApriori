<?php

http_response_code(201);
$JsonReq = array('http_response_code' => 201, 'title' => 'Information', 'message' => 'a!');
print json_encode($JsonReq);
exit();

session_start();

$target_dir = "../Python/dataset/";
$target_file = $target_dir . basename($_FILES["fileToUpload"]["name"]);



if(isset($_POST["submitDataset"])) {
    echo "b";
    if ( isset($_FILES["fileToUpload"])) {
        //if there was an error uploading the file
        if ($_FILES["fileToUpload"]["error"] > 0) {
            echo "Return Code: " . $_FILES["fileToUpload"]["error"] . "<br />";
        }
        else {
            //Print file details
            echo "Upload: " . $_FILES["fileToUpload"]["name"] . "<br />";
            echo "Type: " . $_FILES["fileToUpload"]["type"] . "<br />";
            echo "Size: " . ($_FILES["fileToUpload"]["size"] / 1024) . " Kb<br />";
            echo "Temp file: " . $_FILES["fileToUpload"]["tmp_name"] . "<br />";

            //if file already exists
            if (file_exists($target_dir . $_FILES["fileToUpload"]["name"])) {
                echo $_FILES["fileToUpload"]["name"] . " already exists. ";
            }
            else {
                //Store file in directory "upload" with the name of "uploaded_file.txt"
                $storagename = "uploaded_file.txt";
                move_uploaded_file($_FILES["fileToUpload"]["tmp_name"], $target_file);
                echo "Stored in: " . $target_file . "<br />";
            }
        }
    } 
    else {
        echo "No file selected <br />";
    }
}
?>