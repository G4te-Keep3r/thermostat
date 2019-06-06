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


//get base data
$query = sprintf("CREATE TEMPORARY TABLE tmp SELECT recordID, temp, highCutOff, lowCutOff, temp_hall, outside, attic FROM temp_graphs order by recordID DESC LIMIT 1440");
$result = $mysqli->query($query);


//############## UPDATE tmp set ###=PREWVIOUS ONE where LINE B4 THIS...since sometimes a recordID is not there
//############## find outside with "where outside LIKE 82.2882
#$query = sprintf("UPDATE tmp set outside=(SELECT (temp+highCutOff+lowCutOff+temp_hall+outside)/5.0 from tmp where recordID=419930) where outside LIKE 82.2882");
#$result = $mysqli->query($query);
//(SELECT recordID where outside LIKE 82.2882)

//############## find temp_hall with "where temp_hall LIKE 71.1771
//rare, so add it when it grabs previous record instead of jut the one b4
//$query = sprintf("");
//$result = $mysqli->query($query);

//order by
$query = sprintf("SELECT recordID, temp, highCutOff, lowCutOff, temp_hall, outside, attic FROM tmp ORDER BY tmp.recordID");
$result = $mysqli->query($query);


//$query = sprintf("
//	SELECT recordID, temp, highCutOff, lowCutOff, temp_hall, outside FROM (SELECT recordID, temp, highCutOff, lowCutOff, temp_hall, outside FROM (SELECT recordID, temp, highCutOff, lowCutOff, temp_hall, outside FROM temp_graphs order by recordID DESC LIMIT 1440) tmp1) tmp2 ORDER BY tmp2.recordID;");

//$query = sprintf("
//	SELECT recordID, temp, highCutOff, lowCutOff, temp_hall, outside INTO tmp1 FROM temp_graphs order by recordID DESC LIMIT 1440; 
//	SELECT recordID, temp, highCutOff, lowCutOff, temp_hall, outside INTO tmp2 FROM tmp1; 
//	SELECT recordID, temp, highCutOff, lowCutOff, temp_hall, outside FROM tmp2 ORDER BY tmp2.recordID;");

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