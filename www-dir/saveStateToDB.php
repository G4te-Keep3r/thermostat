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

$sql = "UPDATE temp_graphs SET state='".$_POST["state"]."' WHERE recordID='".$_POST["recordID"]."'";

if ($conn->query($sql) === TRUE) {
    echo "New record created successfully";
} else {
    echo "Error: " . $sql . "<br>" . $conn->error;
}

$conn->close();
?>