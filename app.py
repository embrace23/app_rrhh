from flask import Flask, render_template, request, redirect, url_for, session
from flask_session import Session
from utils import obtener_empleado
import mysql.connector

app = Flask(__name__)
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = True
app.config['SESSION_USE_SIGNER'] = False
app.config['SESSION_KEY_PREFIX'] = 'tu_aplicacion_'
app.secret_key = 'tu_clave_secreta'

Session(app)

@app.route('/')

def index():
    return render_template('index.html')

@app.route('/login', methods = ['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')

    def credenciales_correctas(email, password):
        try:
            conexion = mysql.connector.connect(
                host = "localhost",
                user = "root",
                password = "",
                database = "rrhh"
            )

            if conexion.is_connected():
                cursor = conexion.cursor()

                consulta = "SELECT cuil FROM nomina WHERE mail = %s"
                cursor.execute(consulta, (email,))
                resultado = cursor.fetchone()

                if resultado is not None and resultado[0] == password:
                    return True
                
                cursor.close()

        except mysql.connector.Error as err:
            print(f"Error:{err}")

        finally:
            if 'conexion' in locals():
                conexion.close()
    
        return False

    if credenciales_correctas(email, password):
        session['user'] = email
        return redirect(url_for('inicio'))
    else:
        return "Credenciales incorrectas"
    

#RUTAS A CADA PÁGINA

@app.route('/inicio')
def inicio():
    if 'user' in session:
        usuario = session['user']
        empleado = obtener_empleado(usuario)
        return render_template('inicio.html', usuario=usuario, empleado=empleado)
    else:
        return redirect(url_for('index'))

@app.route('/estudio')
def estudio():
    if 'user' in session:
        usuario = session['user']
        empleado = obtener_empleado(usuario)
        return render_template('estudio.html', usuario=usuario, empleado=empleado)
    else:
        return redirect(url_for('index'))

@app.route('/ausencias')
def ausencias():
    if 'user' in session:
        usuario = session['user']
        empleado = obtener_empleado(usuario)
        return render_template('ausencias.html', usuario=usuario, empleado=empleado)
    else:
        return redirect(url_for('index'))

@app.route('/ajustes')
def ajustes():
    if 'user' in session:
        usuario = session['user']
        empleado = obtener_empleado(usuario)
        return render_template('ajustes.html', usuario=usuario, empleado=empleado)
    else:
        return redirect(url_for('index'))

@app.route('/homeoffice')
def homeoffice():
    if 'user' in session:
        usuario = session['user']
        empleado = obtener_empleado(usuario)
        return render_template('homeoffice.html', usuario=usuario, empleado=empleado)
    else:
        return redirect(url_for('index'))

@app.route('/vacaciones')
def vacaciones():
    if 'user' in session:
        usuario = session['user']
        empleado = obtener_empleado(usuario)
        return render_template('vacaciones.html', usuario=usuario, empleado=empleado)
    else:
        return redirect(url_for('index'))
    
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('index')) 

if __name__ == '__main__':
    app.run(debug=True)