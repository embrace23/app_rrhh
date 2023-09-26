<?php

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $email = $_POST["email"];
    $password = $_POST["password"];

    // Realiza una conexión a la base de datos (Asegúrate de configurar los datos de conexión adecuados)
    $servername = "localhost";
    $username = "id21297990_wmc";
    $password_db = "34Bostero!";
    $database = "id21297990_personal";

    $conn = new mysqli($servername, $username, $password_db, $database);

    if ($conn->connect_error) {
        die("Error de conexión: " . $conn->connect_error);
    }

    // Consulta SQL para buscar el correo y la contraseña en la tabla "nomina"
    $sql = "SELECT cuil FROM empleados WHERE mail = '$email' AND cuil = '$password'";
    $result = $conn->query($sql);

    if ($result->num_rows > 0) {
        // Inicio de sesión exitoso
        header("Location: index.html");
        
        // Puedes redirigir al usuario a una página de inicio de sesión exitoso aquí
    } else {
        // Error de inicio de sesión
        echo "Error de inicio de sesión";
        // Puedes mostrar un mensaje de error o redirigir al usuario a una página de error aquí
    }

    // Cierra la conexión a la base de datos
    $conn->close();
}
?>
