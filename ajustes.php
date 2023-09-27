<?php
session_start();

// Verificar si la sesión está iniciada
if (!isset($_SESSION['email'])) {
    header("Location: index.html");
    exit();
}
?>

<?php
require_once("conexion.php");

// Verificar si el parámetro "email" está presente en la URL
if (isset($_GET['email'])) {
    $email = $_GET['email'];

    // Consulta SQL para obtener el valor de "empleado" cuando "mail" coincide con el valor de "email"
    $sql = "SELECT empleado FROM empleados WHERE mail = '$email'";
    
    // Ejecutar la consulta
    $result = $conn->query($sql);

    // Verificar si se encontró un resultado
    if ($result->num_rows > 0) {
        // Obtener el valor de "empleado" de la primera fila
        $row = $result->fetch_assoc();
        $empleado = $row["empleado"];
    } else {
        // Si no se encontró un resultado, muestra un mensaje de error o realiza alguna otra acción
        echo "No se encontró ningún empleado con el correo $email";
    }
} else {
    // Si el parámetro "email" no está presente en la URL, muestra un mensaje de error o realiza alguna otra acción
    echo "No se proporcionó el correo electrónico en la URL.";
}

// Cerrar la conexión a la base de datos
$conn->close();
?>

<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="styles/styles.css">
    <title>Document</title>
</head>
<body>
    <div id="sidemenu" class="menuCollapsed">
        <!-- Header -->
        <div id="header">
            <div id="menuBtn">
                <div class="btnHamburguesa"></div>
                <div class="btnHamburguesa"></div>
                <div class="btnHamburguesa"></div>
            </div>
            <div id="titulo"><a href="inicio.php?email=<?php echo $email; ?>"><span>Embrace SRL</span></a></div>
        </div>

        <!-- Perfil -->
        <div id="perfil">
            <div id="foto"><a href="inicio.php?email=<?php echo $email; ?>"><img src="images/WMMS.png" alt=""></a></div>
            <div id="nombre"><span><?php echo $empleado; ?></span></div>
        </div>

        <!-- Items -->
        <div id="menuItems">
            <div class="item">
                <div class="icon"><a href="estudio.php?email=<?php echo $email; ?>"><img src="./images/estudio.png" alt=""></a></div>
                <div class="title"><a href="estudio.php?email=<?php echo $email; ?>"><span>Días de estudio</span></a></div>

            </div>

            <div class="item">
                <div class="icon"><a href="homeoffice.php?email=<?php echo $email; ?>"><img src="./images/casa.png" alt=""></a></div>
                <div class="title"><a href="homeoffice.php?email=<?php echo $email; ?>"><span>Home office</span></a></div>
            </div>

            <div class="item">
                <div class="icon"><a href="ausencias.php?email=<?php echo $email; ?>"><img src="./images/ausencia.png" alt=""></a></div>
                <div class="title"><a href="ausencias.php?email=<?php echo $email; ?>"><span>Ausencias</span></a></div>
            </div>

            <div class="item">
                <div class="icon"><a href="vacaciones.php?email=<?php echo $email; ?>"><img src="./images/vacaciones.png" alt=""></a></div>
                <div class="title"><a href="vacaciones.php?email=<?php echo $email; ?>"><span>Vacaciones</span></a></div>
            </div>

            <div class="item">
                <div class="icon"><a href="ajustes.php?email=<?php echo $email; ?>"><img src="./images/configuraciones.png" alt="Ajustes"></a></div>
                <div class="title"><a href="ajustes.php?email=<?php echo $email; ?>"><span>Ajustes</span></a></div>
            </div>
        </div>
    </div>

    <div id="mainContainer">
        AJUSTES
    </div>

    <script src="./js/app.js"></script>
</body>
</html>