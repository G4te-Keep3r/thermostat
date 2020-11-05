<?php
$servername = "localhost";
$username = "ac";
$password = "";
$dbname = "ac";

// Create connection
$conn = new mysqli($servername, $username, $password, $dbname);
// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

$sql = "INSERT INTO temp_graphs (recordID, temp, highCutOff, lowCutOff, temp_hall, outside, attic, state)
VALUES ('".$_POST["recordID"]."', '".$_POST["temp"]."', '".$_POST["highCutOff"]."', '".$_POST["lowCutOff"]."', '".$_POST["temp_hall"]."', '".$_POST["outside"]."', '".$_POST["attic"]."', '".$_POST["state"]."')";



if ($conn->query($sql) === TRUE) {
    echo "New record created successfully";
} else {
    echo "Error: " . $sql . "<br>" . $conn->error;
}

$conn->close();
?>
