import mysql.connector

#Función para obtener el nombre del empleado en base a quien inicio sesión
def obtener_empleado(correo):
    try:
        conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="rrhh"
        )

        if conexion.is_connected():
            cursor = conexion.cursor()

            consulta = "SELECT empleado FROM nomina WHERE mail = %s"
            cursor.execute(consulta, (correo,))
            resultado = cursor.fetchone()

            if resultado:
                empleado = resultado[0]
            else:
                empleado = "Nombre de usuario no encontrado"

            cursor.close()

        else:
            empleado = "Error en la conexión a la base de datos"

    except mysql.connector.Error as err:
        empleado = f"Error: {err}"

    finally:
        if 'conexion' in locals():
            conexion.close()

    return empleado

#Función para guardar la fecha segun el empleado
def guardar_fecha(usuario, fecha):
    try:
        conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="rrhh"
        )

        if conexion.is_connected():
            cursor = conexion.cursor()

            # Inserta la fecha en la tabla dia_estudio
            consulta = "INSERT INTO dia_estudio (empleado, fecha) VALUES (%s, %s)"
            cursor.execute(consulta, (usuario, fecha))

            # Realiza el commit para guardar los cambios
            conexion.commit()

            cursor.close()
            return True  # La fecha se guardó correctamente

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        if 'conexion' in locals():
            conexion.close()

    return False  # Hubo un error al guardar la fecha