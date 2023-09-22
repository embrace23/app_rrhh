import mysql.connector

# Configura la conexión a la base de datos
db_connection = mysql.connector.connect(
   host="localhost",
   user="root",
   password="",
   database="rrhh"
)

# Crea un cursor
cursor = db_connection.cursor()

# Ejecuta una consulta SQL
cursor.execute("SELECT * FROM nomina")

# Recupera resultados
results = cursor.fetchall()

# Imprime los resultados
for row in results:
    print(row)

# Cierra el cursor y la conexión
cursor.close()
db_connection.close()
