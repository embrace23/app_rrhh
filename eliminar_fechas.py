import schedule
import time
import datetime
import mysql.connector

def eliminar_fechas_antiguas():
    try:
        conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="rrhh"
        )

        if conexion.is_connected():
            cursor = conexion.cursor()

            # Calcular la fecha límite (hace 90 días)
            limite = datetime.datetime.now() - datetime.timedelta(days=90)

            # Consulta para eliminar fechas antiguas
            consulta = "DELETE FROM dia_estudio WHERE fecha < %s"
            cursor.execute(consulta, (limite,))

            conexion.commit()
            cursor.close()

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        if 'conexion' in locals():
            conexion.close()