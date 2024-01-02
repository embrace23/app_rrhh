import schedule
import time
from datetime import datetime
import mysql.connector
from openpyxl import Workbook
from io import BytesIO

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
def guardar_fecha(usuario, fecha, area, jerarquia, pagina, aprobado=None):
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


            if aprobado:
                consulta = f"INSERT INTO dias_pedidos (empleado, fecha, area, jerarquia, fecha_modificacion, concepto, aprobado) VALUES (%s, %s, %s, %s, NOW(), %s, %s)"
                cursor.execute(consulta, (usuario, fecha, area, jerarquia, pagina, aprobado))
            else:
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
def obtener_dias_pedidos(concepto, area=None, nombre_empleado=None, aprobado=None):
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
                if aprobado == "SI":
                    consulta = "SELECT fecha FROM dias_pedidos WHERE empleado = %s AND concepto = %s AND aprobado = 'SI'"
                elif aprobado == "NO":
                    consulta = "SELECT fecha FROM dias_pedidos WHERE empleado = %s AND concepto = %s AND aprobado = 'NO'"
                cursor.execute(consulta, (nombre_empleado, concepto))
            else:
                if area:
                    consulta = "SELECT empleado, fecha FROM dias_pedidos WHERE concepto = %s AND area = %s AND aprobado = 'SI'"
                    cursor.execute(consulta, (concepto, area))
                else:
                    consulta = "SELECT empleado, fecha FROM dias_pedidos WHERE concepto = %s AND aprobado = 'SI'"
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
def obtener_vacaciones(area=None, nombre_empleado=None):
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

            if nombre_empleado:
                consulta = "SELECT fecha_inicio, fecha_fin FROM vacaciones WHERE empleado = %s and aprobado = 'SI'"
                cursor.execute(consulta, (nombre_empleado,))
            
            if area:
                consulta = "SELECT empleado, fecha_inicio, fecha_fin FROM vacaciones WHERE area = %s AND aprobado = 'SI'"
                cursor.execute(consulta, (area,))
            else:
                consulta = "SELECT empleado, fecha_inicio, fecha_fin FROM vacaciones WHERE aprobado = 'SI'"
                cursor.execute(consulta)
                    
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
def obtener_personal(area=None):
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
            if area:
                consulta = "SELECT empleado FROM nomina WHERE area = %s AND cuenta = 'SI'"
                cursor.execute(consulta, (area,))
            else:
                consulta = "SELECT empleado FROM nomina WHERE cuenta = 'SI'"
                cursor.execute(consulta)
            
            # Recupera los nombres de empleados
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

            consulta = "SELECT empleado, legajo, mail, forma, turno, area, jerarquia, equipo, convenio FROM nomina WHERE empleado = %s"
            cursor.execute(consulta, (empleado,))
            resultado = cursor.fetchone()

            if resultado:
                datos_empleado = {
                    'empleado': resultado[0],
                    'legajo': resultado[1],
                    'mail': resultado[2],
                    'forma': resultado[3],
                    'turno': resultado[4],
                    'area': resultado[5],
                    'jerarquia': resultado[6],
                    'equipo': resultado[7],
                    'convenio': resultado[8]
                }
                return datos_empleado

            cursor.close()

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        if 'conexion' in locals():
            conexion.close()

    return None

#Función para actualizar la cuenta
def actualizar_cuenta(empleado):
    try:
        conexion = mysql.connector.connect(
            host = 'localhost',
            user = 'root',
            password = '',
            database = 'rrhh'
        )

        if conexion.is_connected():
            cursor = conexion.cursor()
            
            consulta = "UPDATE nomina SET cuenta = 'NO' WHERE empleado = %s"
            cursor.execute(consulta, (empleado,))

            conexion.commit()

            cursor.close()
    
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if conexion in locals():
            conexion.close()
    
#Función para cargar los datos en la base de datos si se decide modificar
def actualizar_datos_empleado(empleado, legajo, mail, forma, turno, area, jerarquia, equipo, convenio):
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
                SET legajo = %s, mail = %s, forma = %s, turno = %s, area = %s, jerarquia = %s, equipo = %s, convenio = %s
                WHERE empleado = %s
            """
            valores = (legajo, mail, forma, turno, area, jerarquia, equipo, convenio, empleado)

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

#Funcion para traer los dias que necesitan autorizacion aun
def dias_por_autorizar(area=None):
    dias_a_autorizar = []
    try:
        conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="rrhh"
        )

        if conexion.is_connected():
            cursor = conexion.cursor()

            if area:
                consulta = "SELECT empleado, fecha, fecha_modificacion, concepto FROM dias_pedidos WHERE area = %s AND aprobado = 'NO'"
                cursor.execute(consulta, (area,))
            else:
                consulta = "SELECT empleado, fecha, fecha_modificacion, concepto FROM dias_pedidos WHERE aprobado = 'NO' or aprobado = 'Aprobado por Gerencia'"
                cursor.execute(consulta)

            resultados = cursor.fetchall()

            for resultado in resultados:
                empleado, fecha, fecha_modificacion, concepto = resultado
                dias_a_autorizar.append({'empleado': empleado, 'fecha': fecha, 'fecha_modificacion': fecha_modificacion[:10], 'concepto': concepto})

            cursor.close()
            return dias_a_autorizar

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        if 'conexion' in locals():
            conexion.close()
    return dias_a_autorizar

#Funcion para trar las vacaciones que necesitan autorizacion aun
def vacaciones_por_autorizar(area=None):
    vacaciones_a_autorizar = []
    try:
        conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="rrhh"
        )

        if conexion.is_connected():
            cursor = conexion.cursor()

            if area:
                consulta = "SELECT empleado, fecha_inicio, fecha_fin , fecha_modificacion FROM vacaciones WHERE area = %s AND aprobado = 'NO'"
                cursor.execute(consulta, (area,))
            else:
                consulta = "SELECT empleado, fecha_inicio, fecha_fin, fecha_modificacion FROM vacaciones WHERE aprobado = 'NO'"
                cursor.execute(consulta)

            resultados = cursor.fetchall()

            for resultado in resultados:
                empleado, fecha_inicio, fecha_fin, fecha_modificacion = resultado
                vacaciones_a_autorizar.append({'empleado': empleado, 'fecha_inicio': fecha_inicio, 'fecha_fin': fecha_fin, 'fecha_modificacion': fecha_modificacion[:10]})

            cursor.close()
            return vacaciones_a_autorizar

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        if 'conexion' in locals():
            conexion.close()
    return vacaciones_a_autorizar

#Funcion para aprobar los dias
def aprobar_solicitud(empleado, fecha, concepto, jerarquia, gerente):
    try:
        conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="rrhh"
        )

        if conexion.is_connected():
            cursor = conexion.cursor()

            fecha_hora_actual = datetime.now()

            fecha_hora_actual_str = fecha_hora_actual.strftime("%Y-%m-%d %H:%M:%S")

            if concepto != "vacaciones":
                if jerarquia:
                    consulta = "UPDATE dias_pedidos SET aprobado = 'SI', fecha_cambio_estado = %s, gerente = %s WHERE empleado = %s AND fecha = %s AND concepto = %s"
                    cursor.execute(consulta, (fecha_hora_actual_str, gerente, empleado, fecha, concepto))
            elif concepto == "vacaciones":
                consulta = "UPDATE vacaciones SET aprobado = 'SI', fecha_cambio_estado = %s, gerente = %s WHERE empleado = %s AND fecha_inicio = %s"
                cursor.execute(consulta, (fecha_hora_actual_str, gerente, empleado, fecha))
            conexion.commit()

            cursor.close()
    
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    
    finally:
        if 'conexion' in locals():
            conexion.close()

#Funcion para eliminar la solicitud
def eliminar_solicitud(empleado, fecha, concepto):
    try:
        conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="rrhh"
        )

        if conexion.is_connected():
            cursor = conexion.cursor()

            if concepto != "vacaciones":
                consulta = "UPDATE dias_pedidos SET aprobado = 'RECHAZADO' WHERE empleado = %s and fecha = %s and concepto = %s"
                cursor.execute(consulta, (empleado, fecha, concepto))
            elif concepto == "vacaciones":
                consulta = "UPDATE vacaciones SET aprobado = 'RECHAZADO' WHERE empleado = %s and fecha_inicio = %s"
                cursor.execute(consulta, (empleado, fecha))
            conexion.commit()

            cursor.close()
    
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    
    finally:
        if 'conexion' in locals():
            conexion.close()

#Funcion para guardar excel
def obtener_nomina_y_generar_excel():
    try:
        conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="rrhh"
        )

        if conexion.is_connected():
            cursor = conexion.cursor()

            consulta = "SELECT * FROM nomina WHERE cuenta = 'SI'"
            cursor.execute(consulta)
            nomina = cursor.fetchall()

            output = generar_excel(nomina)

            cursor.close()

            return output
    
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    
    finally:
        if 'conexion' in locals():
            conexion.close()

def generar_excel(nomina):
    workbook = Workbook()
    sheet = workbook.active

    encabezados = ["Empleado", "Cuil", "Fecha_ingreso", "Finaliza_pp", "Legajo", "Mail", "Cuenta", "Genero", "Fecha_nacimiento", "Forma", "Turno", "Area", "Jerarquia", "Equipo", "Convenio", "Contrasena"]
    sheet.append(encabezados)

    for fila in nomina:
        sheet.append(fila)

    output = BytesIO()
    workbook.save(output)
    output.seek(0)

    return output

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