<html>
<head><title>CS 23200/33250 sink HW5</title></head>
<body>
<?php
header("Access-Control-Allow-Origin: *");

$servername = "localhost";
$username = "lynn";
$password = "insecurity232";

// Create connection
$conn = new mysqli($servername, $username, $password);

// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}
echo "Connected successfully";

$conn->select_db("hw5_db");

$table_name = "problem4";

$page = $_GET["page"];
$cookie = $_GET["cookie"];
$ip = $_GET["ip"];
$user_agent = $_GET["user_agent"];
$do_not_track = $_GET["do_not_track"]; // could be unspecified or null, not bool
$fonts = $_GET["fonts"];

$window_width = filter_var($_GET["window_width"], FILTER_VALIDATE_INT);
$window_height = filter_var($_GET["window_height"], FILTER_VALIDATE_INT);

$enable_cookie = filter_var($_GET["enable_cookie"], FILTER_VALIDATE_BOOLEAN);
$enable_popup = filter_var($_GET["enable_popup"], FILTER_VALIDATE_BOOLEAN);

$sql = "INSERT INTO $table_name (page, cookie, ip, window_width, window_height, user_agent, enable_cookie, do_not_track, enable_popup, fonts) 
VALUES ('$page', '$cookie', '$ip', '$window_width', '$window_height', '$user_agent', '$enable_cookie', '$do_not_track', '$enable_popup', '$fonts')";

if ($conn->query($sql) === TRUE) {
    echo "New record created successfully";
} else {
    echo "Error: " . $sql . "<br>" . $conn->error;
}

$conn->close();
?>
</body>
</html>
