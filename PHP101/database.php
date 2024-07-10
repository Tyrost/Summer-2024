<?php
    $db_server = "localhost";
    $db_user = "root";
    $db_passw = "";
    $db_name = "summer2024db";

    
    $conn = mysqli_connect($db_server, $db_user, $db_passw, $db_name);

    
    if (!$conn) {
        die("Connection failed: " . mysqli_connect_error());
    } else {
        echo "Connected successfully";
    }


    function main() {
        global $conn;

        function generate_id() {
            $result = '';
            for ($i = 0; $i<6; $i++) {
                $num = random_int(0,9);
    
                $result .= $num;
            }
            return ($result);
        }
        
    
        if ($_SERVER['REQUEST_METHOD'] == 'POST') {
            $username = filter_input(INPUT_POST, 'username', FILTER_SANITIZE_SPECIAL_CHARS);
            $password = filter_input(INPUT_POST, 'password', FILTER_SANITIZE_SPECIAL_CHARS);
        
            if (empty($username) || empty($password)) {
                echo "Please enter required fields";
            } else {
                $pw_hash = password_hash($password, PASSWORD_DEFAULT);
    
                do {
    
                    $id = generate_id();
                    $check_id_sql = "SELECT * FROM ids WHERE user_id = '$id'";
                    $result = mysqli_query($conn, $check_id_sql);
                    }
    
                while (mysqli_num_rows($result) > 0);
                    $sql = "INSERT INTO users (user_id, username, password) 
                    VALUES ('$id', '$username', '$pw_hash')";
                    $sql_id = "INSERT INTO ids (user_id) VALUES ('$id')";
                
        
                $sql = "INSERT INTO users (user_id, username, password) 
                        VALUES ('$id', '$username', '$pw_hash')";
    
                $sql_id = "INSERT INTO ids (user_id) VALUES ('$id')";
                try {
                    if (mysqli_query($conn, $sql) && mysqli_query($conn, $sql_id)) {
                        echo 'User now registered';
                    } else {
                        echo 'Error: ' . mysqli_error($conn);
                    }
                } catch(mysqli_sql_exception) {
                    echo "Username already taken";
                }

            }
        }
    }
    
?>
