import mysql.connector

try:
    conexion = mysql.connector.connect(
        host="localhost",
        user="root",   
        password="",  
        database="rrhh"
    )

    if conexion.is_connected():
        print("Conexión exitosa a la base de datos")

        cursor = conexion.cursor()

        consulta = "SELECT mail FROM nomina LIMIT 5"
        cursor.execute(consulta)

        top_5_resultados = cursor.fetchall()

        for fila in top_5_resultados:
            print(fila)

        cursor.close()

except mysql.connector.Error as err:
    print(f"Error: {err}")

finally:
    if 'conexion' in locals():
        conexion.close()