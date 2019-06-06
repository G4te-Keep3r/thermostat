<?php
//setting header to json
header('Content-Type: application/json');

//database
define('DB_HOST', 'localhost');
define('DB_USERNAME', 'ac');
define('DB_PASSWORD', 'toor');
define('DB_NAME', 'ac');

//get connection
$mysqli = new mysqli(DB_HOST, DB_USERNAME, DB_PASSWORD, DB_NAME);

if(!$mysqli){
	die("Connection failed: " . $mysqli->error);
}

//query to get data from the table
//$query = sprintf("SELECT userid, facebook, twitter, googleplus FROM followers");
$query = sprintf("SELECT recordID, temp, highCutOff, lowCutOff, temp_hall, outside, attic FROM (SELECT recordID, temp, highCutOff, lowCutOff, temp_hall, outside, attic FROM temp_graphs order by recordID DESC LIMIT 4320) tmp ORDER BY tmp.recordID");

//execute query
$result = $mysqli->query($query);

//loop through the returned data
$data = array();
foreach ($result as $row) {
	$data[] = $row;
}

//free memory associated with result
$result->close();

//close connection
$mysqli->close();

//now print the data
print json_encode($data);