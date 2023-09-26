<?php

require_once("conexion.php");

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $email = $_POST["email"];
    $password = $_POST["password"];

    // Consulta SQL para buscar el correo y la contraseña en la tabla "nomina"
    $sql = "SELECT cuil, empleado FROM empleados WHERE mail = '$email' AND cuil = '$password'";
    $result = $conn->query($sql);

    if ($result->num_rows > 0) {
        
        header("Location: inicio.php?email=$email");
        
    } else {
        echo "Error de inicio de sesión";
    }

    $conn->close();
}
?>
