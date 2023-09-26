<?php
$servername = "localhost";
$username = "id21297990_wmc";
$password_db = "34Bostero!";
$database = "id21297990_personal";

// Crear una conexión a la base de datos
$conn = new mysqli($servername, $username, $password_db, $database);

// Verificar la conexión
if ($conn->connect_error) {
    die("Error de conexión: " . $conn->connect_error);
}
?>