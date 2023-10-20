import schedule
import time
from datetime import datetime
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

#Funcion para obtener la jerarquia del empleado
def obtener_area_jerarquia(correo):
    try:
        conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="rrhh"
        )

        if conexion.is_connected():
            cursor = conexion.cursor()

            consulta = "SELECT area, jerarquia FROM nomina WHERE mail = %s"
            cursor.execute(consulta, (correo,))
            resultado = cursor.fetchone()

            if resultado:
                area = resultado[0]
                jerarquia = resultado[1]
            else:
                jerarquia = "Mail de usuario no encontrado"

            cursor.close()

        else:
            jerarquia = "Error en la conexión a la base de datos"

    except mysql.connector.Error as err:
        jerarquia = f"Error: {err}"

    finally:
        if 'conexion' in locals():
            conexion.close()

    return (area, jerarquia)

#Función para guardar la fecha segun el empleado
def guardar_fecha(usuario, fecha, area, jerarquia, pagina):
    try:
        conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="rrhh"
        )
        """
        if pagina == 'estudio':
            tabla = 'dia_estudio'
        elif pagina == 'homeoffice':
            tabla = 'home'
        elif pagina == 'ausencias':
            tabla = 'ausencias'
        """

        if conexion.is_connected():
            cursor = conexion.cursor()

            consulta = f"INSERT INTO dias_pedidos (empleado, fecha, area, jerarquia, fecha_modificacion, concepto) VALUES (%s, %s, %s, %s, NOW(), %s)"
            cursor.execute(consulta, (usuario, fecha, area, jerarquia, pagina))

            conexion.commit()

            cursor.close()
            return True  

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        if 'conexion' in locals():
            conexion.close()

    return False

#Funcion para obtener los dias pedidos por el empleado de la tabla general
def obtener_dias_pedidos(concepto, area=None, nombre_empleado=None):
    dias_pedidos = []

    try:
        conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="rrhh"
        )

        if conexion.is_connected():
            cursor = conexion.cursor()

            if nombre_empleado:
                consulta = "SELECT fecha FROM dias_pedidos WHERE empleado = %s AND concepto = %s"
                cursor.execute(consulta, (nombre_empleado, concepto))
            else:
                consulta = "SELECT empleado, fecha FROM dias_pedidos WHERE concepto = %s"
                cursor.execute(consulta, (concepto,))

            resultados = cursor.fetchall()

            for resultado in resultados:
                if nombre_empleado:
                    dias_pedidos.append(resultado[0])
                else:
                    empleado = resultado[0]
                    fecha = resultado[1]
                    dias_pedidos.append((empleado, fecha))

            cursor.close()

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        if 'conexion' in locals():
            conexion.close()

    return dias_pedidos

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

#Función para obtener todo el personal de la empresa
def obtener_personal():
    empleados = []
    
    try:
        conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="rrhh"
        )

        if conexion.is_connected():
            cursor = conexion.cursor()
            
            # Consulta para obtener los nombres de los empleados desde la tabla "nomina"
            consulta = "SELECT empleado FROM nomina"
            cursor.execute(consulta)
            
            # Recupera todos los nombres de empleados
            resultados = cursor.fetchall()
            
            for resultado in resultados:
                empleados.append(resultado[0])

            cursor.close()

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        if 'conexion' in locals():
            conexion.close()

    return empleados

#Función para traer la información personal del empleado que se seleccionó en el menú desplegable
def obtener_datos(empleado):
    try:
        conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="rrhh"
        )

        if conexion.is_connected():
            cursor = conexion.cursor()

            # Definir la consulta SQL para seleccionar los datos del empleado
            consulta = "SELECT empleado, cuenta, forma, turno, area, equipo, convenio, legajo, mail FROM nomina WHERE empleado = %s"
            cursor.execute(consulta, (empleado,))
            resultado = cursor.fetchone()  # Suponemos que el empleado es único

            # Verificar si se encontró información del empleado
            if resultado:
                datos_empleado = {
                    'empleado': resultado[0],
                    'cuenta': resultado[1],
                    'forma': resultado[2],
                    'turno': resultado[3],
                    'area': resultado[4],
                    'equipo': resultado[5],
                    'convenio': resultado[6],
                    'legajo': resultado[7],
                    'mail': resultado[8]
                }
                return datos_empleado

            cursor.close()

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        if 'conexion' in locals():
            conexion.close()

    return None

#Función para cargar los datos en la base de datos si se decide modificar
def actualizar_datos_empleado(nombre, cuenta, forma, turno, area, equipo, convenio, legajo, mail):
    try:
        conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="rrhh"
        )

        if conexion.is_connected():
            cursor = conexion.cursor()

            # Query para actualizar los datos del empleado
            consulta = """
                UPDATE nomina
                SET cuenta = %s, forma = %s, turno = %s, area = %s, equipo = %s, convenio = %s, legajo = %s, mail = %s
                WHERE empleado = %s
            """
            valores = (cuenta, forma, turno, area, equipo, convenio, legajo, mail, nombre)

            cursor.execute(consulta, valores)
            conexion.commit()

            cursor.close()
            return True  # Actualización exitosa

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        if 'conexion' in locals():
            conexion.close()

    return False  # Hubo un error en la actualización

""""
def registrar_inicio_sesion(usuario):
    try:
        conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="rrhh"
        )

        if conexion.is_connected():
            cursor = conexion.cursor()

            # Obtiene la hora actual
            hora_actual = datetime.now()
            hora_actual_form = hora_actual.strftime("%Y-%m-%d %H:%M:%S")

            # Inserta el registro en la tabla inicio_sesion
            consulta = "INSERT INTO inicio_sesion (empleado, fecha_hora) VALUES (%s, %s)"
            valores = (usuario, hora_actual_form)

            cursor.execute(consulta, valores)
            conexion.commit()

            cursor.close()
    except mysql.connector.Error as err:
        print(f"Error: {err}")
"""