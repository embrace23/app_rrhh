import schedule
import time
import datetime
import mysql.connector

#Función para chequear que el mail y la contraseña sean los correctos
def verificar_credenciales(email, password):
    try:
        conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="rrhh"
        )

        if conexion.is_connected():
            cursor = conexion.cursor()

            consulta = "SELECT contrasena FROM nomina WHERE mail = %s"
            cursor.execute(consulta, (email,))
            resultado = cursor.fetchone()

            if resultado is not None and resultado[0] == password:
                return True

            cursor.close()

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        if 'conexion' in locals():
            conexion.close()

    return False

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
def guardar_fecha(usuario, fecha, pagina):
    try:
        conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="rrhh"
        )

        if pagina == 'estudio':
            tabla = 'dia_estudio'
        elif pagina == 'homeoffice':
            tabla = 'home'
        elif pagina == 'ausencias':
            tabla = 'ausencias'

        if conexion.is_connected():
            cursor = conexion.cursor()

            consulta = f"INSERT INTO {tabla} (empleado, fecha) VALUES (%s, %s)"
            cursor.execute(consulta, (usuario, fecha))

            conexion.commit()

            cursor.close()
            return True  

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        if 'conexion' in locals():
            conexion.close()

    return False

#Función para generar la tabla según los dias de estudio solicitados por el empleado
def obtener_dias_estudio(nombre_empleado):
    dias_estudio = []
    try:
        conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="rrhh"
        )

        if conexion.is_connected():
            cursor = conexion.cursor()

            consulta = "SELECT fecha FROM dia_estudio WHERE empleado = %s"
            cursor.execute(consulta, (nombre_empleado,))
            resultados = cursor.fetchall()

            for resultado in resultados:
                dias_estudio.append(resultado[0])

            cursor.close()

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        if 'conexion' in locals():
            conexion.close()

    return dias_estudio

#Función para generar la tabla según los dias de homeoffice solicitados por el empleado
def obtener_homeoffice(nombre_empleado):
    homeoffice = []
    try:
        conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="rrhh"
        )

        if conexion.is_connected():
            cursor = conexion.cursor()

            consulta = "SELECT fecha FROM home WHERE empleado = %s"
            cursor.execute(consulta, (nombre_empleado,))
            resultados = cursor.fetchall()

            for resultado in resultados:
                homeoffice.append(resultado[0])

            cursor.close()

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        if 'conexion' in locals():
            conexion.close()

    return homeoffice

#Función para generar la tabla según los dias de ausencia solicitados por el empleado
def obtener_ausencias(nombre_empleado):
    ausencias = []
    try:
        conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="rrhh"
        )

        if conexion.is_connected():
            cursor = conexion.cursor()

            consulta = "SELECT fecha FROM ausencias WHERE empleado = %s"
            cursor.execute(consulta, (nombre_empleado,))
            resultados = cursor.fetchall()

            for resultado in resultados:
                ausencias.append(resultado[0])

            cursor.close()

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        if 'conexion' in locals():
            conexion.close()

    return ausencias

#Función para generar la tabla según los dias de vacaciones solicitados por el empleado
def obtener_vacaciones(nombre_empleado):
    vacaciones = []
    try:
        conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="rrhh"
        )

        if conexion.is_connected():
            cursor = conexion.cursor()

            consulta = "SELECT fecha_inicio, fecha_fin FROM vacaciones WHERE empleado = %s"
            cursor.execute(consulta, (nombre_empleado,))
            resultados = cursor.fetchall()

            for resultado in resultados:
                vacaciones.append(resultado)

            cursor.close()

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        if 'conexion' in locals():
            conexion.close()

    return vacaciones

#Función para insertar los dias de vacaciones a la tabla correspondiente
def insertar_registro(tabla, campos):
    try:
        conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="rrhh"
        )

        if conexion.is_connected():
            cursor = conexion.cursor()

            campos_nombres = ', '.join(campos.keys())
            campos_valores = ', '.join(['%s'] * len(campos))

            consulta = f"INSERT INTO {tabla} ({campos_nombres}) VALUES ({campos_valores})"
            valores = tuple(campos.values())

            cursor.execute(consulta, valores)
            conexion.commit()

            cursor.close()
            return True
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if 'conexion' in locals():
            conexion.close()
    return False

# Función para verificar si una contraseña cumple con requisitos de seguridad (personalizar según tus criterios)
def cumple_requisitos_seguridad(password):
    # Aquí debes implementar tus criterios de seguridad, por ejemplo, longitud mínima, caracteres especiales, etc.
    if len(password) >= 8:
        return True
    else:
        return False

# Función para actualizar la contraseña en la base de datos
def actualizar_contrasena(usuario, contrasena_nueva):
    try:
        conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="rrhh"  # Reemplaza con el nombre de tu base de datos
        )

        if conexion.is_connected():
            cursor = conexion.cursor()

            # Actualizar la contraseña en la base de datos
            consulta = "UPDATE nomina SET contrasena = %s WHERE mail = %s"
            cursor.execute(consulta, (contrasena_nueva, usuario))
            conexion.commit()

            cursor.close()
            return True  # Contraseña actualizada con éxito

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        if 'conexion' in locals():
            conexion.close()

    return False  # Hubo un error en la actualización de la contraseña


