var curl1="curl -X POST \
https://nireas.it.teithe.gr/webapriori/webAPI/APIuploadDataset.php \
-H 'cache-control: no-cache' \
-H 'content-type: multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW' \
-F email=##1## \
-F apiKey=##2## \
-F fileToUpload=@/TheAbsoluteFilePath.csv \
-F datasetType=##3##";