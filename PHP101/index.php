<?php

    session_start();
    include('database.php');
?>


<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>
<body>
    <h2>This is the login page</h2><br>
    <h1 name="title" value='title'>ALPHA DESIGNS</h1>
    <!-- <a href="./home.php">This takes you home</a> -->
    <hr>

    <form action="index.php" method="post">
        <label>username: </label>
        <input type="text" name="username"><br>
        <label>password:</label>
        <input type='password' name="password"><br>
        <input type="submit" name="login" value="login">
    </form>

</body>
</html>
    
<?php

main() 

?>

