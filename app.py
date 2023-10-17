from flask import Flask, render_template, request, redirect, url_for, session
from flask_session import Session
from utils import obtener_empleado, guardar_fecha, obtener_dias_estudio, verificar_credenciales, obtener_homeoffice, obtener_ausencias, obtener_vacaciones, insertar_registro, actualizar_contrasena, cumple_requisitos_seguridad, obtener_personal, obtener_datos, actualizar_datos_empleado, registrar_inicio_sesion
import mysql.connector
from datetime import datetime, timedelta

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

    if verificar_credenciales(email, password):
        session['user'] = email
        registrar_inicio_sesion(email)
        return redirect(url_for('inicio'))
    else:
        return "Credenciales incorrectas"
    

#RUTA A INICIO
@app.route('/inicio')
def inicio():
    if 'user' in session:
        usuario = session['user']
        empleado = obtener_empleado(usuario)
        return render_template('inicio.html', usuario=usuario, empleado=empleado)
    else:
        return redirect(url_for('index'))
    
#RUTA A ESTUDIO
@app.route('/estudio')
def estudio():
    if 'user' in session:
        usuario = session['user']
        empleado = obtener_empleado(usuario)
        dias_estudio = obtener_dias_estudio(empleado)
        eliminar_registros_antiguos('dia_estudio')
        return render_template('estudio.html', usuario=usuario, empleado=empleado, dias_estudio=dias_estudio)
    else:
        return redirect(url_for('index'))
    
#RUTA A AUSENCIAS
@app.route('/ausencias')
def ausencias():
    if 'user' in session:
        usuario = session['user']
        empleado = obtener_empleado(usuario)
        ausencias = obtener_ausencias(empleado)
        eliminar_registros_antiguos('ausencias')
        return render_template('ausencias.html', usuario=usuario, empleado=empleado, ausencias=ausencias)
    else:
        return redirect(url_for('index'))

#RUTA A AJUSTES
@app.route('/ajustes')
def ajustes():
    if 'user' in session:
        usuario = session['user']
        empleado = obtener_empleado(usuario)
        return render_template('ajustes.html', usuario=usuario, empleado=empleado)
    else:
        return redirect(url_for('index'))

#RUTA A HOMEOFFICE
@app.route('/homeoffice')
def homeoffice():
    if 'user' in session:
        usuario = session['user']
        empleado = obtener_empleado(usuario)
        homeoffice = obtener_homeoffice(empleado)
        eliminar_registros_antiguos('home')
        return render_template('homeoffice.html', usuario=usuario, empleado=empleado, homeoffice=homeoffice)
    else:
        return redirect(url_for('index'))

#RUTA A VACACIONES
@app.route('/vacaciones')
def vacaciones():
    if 'user' in session:
        usuario = session['user']
        empleado = obtener_empleado(usuario)
        vacaciones = obtener_vacaciones(empleado)
        eliminar_registros_antiguos('vacaciones')
        return render_template('vacaciones.html', usuario=usuario, empleado=empleado, vacaciones=vacaciones)
    else:
        return redirect(url_for('index'))
    
#RUTA A EDITAR
@app.route('/editar')
def editar():
    if 'user' in session:
        usuario = session['user']
        empleado = obtener_empleado(usuario)
        personal = obtener_personal()
        return render_template('editar.html', usuario=usuario, empleado=empleado, personal=personal)
    else:
        return redirect(url_for('index'))

#CIERRE DE SESION   
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))

#GUARDAR FECHA AL HACER CLIC EN EL BOTÓN
@app.route('/guardar_fecha', methods=['POST'])
def guardar_fecha_route():
    return guardar_fecha_generico('estudio', 'fecha')
    
@app.route('/guardar_home', methods=['POST'])
def guardar_home_route():
    return guardar_fecha_generico('homeoffice', 'fechaHome')

@app.route('/guardar_ausencias', methods=['POST'])
def guardar_ausencias_route():
    return guardar_fecha_generico('ausencias', 'fechaAusencias')

def guardar_fecha_generico(pagina, campo_fecha):
    if 'user' in session:
        correo = session['user']
        nombre_empleado = obtener_empleado(correo)
        fecha = request.form.get(campo_fecha)

        resultado = guardar_fecha(nombre_empleado, fecha, pagina)

        if resultado:
            return redirect(url_for(pagina))
        else:
            return "Error al guardar la fecha"
    else:
        return redirect(url_for('index'))
    
@app.route('/guardar_vacaciones', methods=['POST'])
def guardar_vacaciones():
    if 'user' in session:
        correo = session['user']
        nombre_empleado = obtener_empleado(correo)
        
        fecha_inicio = request.form.get('fecha_inicio')
        fecha_fin = request.form.get('fecha_fin')

        if fecha_inicio and fecha_fin:
            tabla = 'vacaciones'

            fecha_modificacion = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            campos = {
                'empleado': nombre_empleado,
                'fecha_inicio': fecha_inicio,
                'fecha_fin': fecha_fin,
                'fecha_modificacion': fecha_modificacion
            }
            resultado = insertar_registro(tabla, campos)

            if resultado:
                return redirect(url_for('vacaciones'))
            else:
                return "Error al guardar las fechas de vacaciones"
        else:
            return "Debes proporcionar ambas fechas de inicio y fin"
    else:
        return redirect(url_for('index'))


@app.route('/cambiar_contrasena', methods=['POST'])
def cambiar_contrasena():
    if 'user' in session:
        usuario = session['user']
        password_actual = request.form.get('password_actual')
        password_nueva = request.form.get('password_nueva')
        password_nueva_repetir = request.form.get('password_nueva_repetir')
        
        if verificar_credenciales(usuario, password_actual):
            if password_nueva == password_nueva_repetir:
                if cumple_requisitos_seguridad(password_nueva):
                    if actualizar_contrasena(usuario, password_nueva):
                        return "Contraseña cambiada exitosamente"
                    else:
                        return "Error al actualizar la contraseña en la base de datos"
                else:
                    return "La nueva contraseña no cumple con los requisitos de seguridad"
            else:
                return "Las contraseñas nuevas no coinciden"
        else:
            return "La contraseña actual es incorrecta"

    else:
        return redirect(url_for('index'))

@app.route('/editar_informacion', methods=['POST'])
def editar_informacion():
    if request.method == 'POST':
        empleado_editar =  request.form.get('empleado')

        if empleado_editar:
            informacion_empleado = obtener_datos(empleado_editar)
            if informacion_empleado:
                if 'user' in session:
                    usuario = session['user']
                    empleado = obtener_empleado(usuario)
                    personal = obtener_personal()
                    return render_template('editar.html', usuario=usuario, empleado=empleado, personal=personal, datos=informacion_empleado)
                else:
                    return redirect(url_for('index'))

@app.route('/guardar_informacion', methods=['POST'])
def guardar_informacion():
    if request.method == 'POST':
        # Obtén los datos actualizados del formulario
        nombre = request.form.get('empleado')
        cuenta = request.form.get('cuenta')
        forma = request.form.get('forma')
        turno = request.form.get('turno')
        area = request.form.get('area')
        equipo = request.form.get('equipo')
        convenio = request.form.get('convenio')
        legajo = request.form.get('legajo')
        mail = request.form.get('mail')

        # Realiza la actualización en la base de datos (debes implementar esta función)
        exito_actualizacion = actualizar_datos_empleado(nombre, cuenta, forma, turno, area, equipo, convenio, legajo, mail)

        if exito_actualizacion:
            # Si la actualización fue exitosa, redirige a una página de confirmación
            return redirect(url_for('editar'))
        else:
            # Si hubo un error en la actualización, puedes manejarlo aquí
            # Por ejemplo, mostrar un mensaje de error y redirigir a una página de error
            return redirect(url_for('editar'))

def eliminar_registros_antiguos(tabla):
    try:
        conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="rrhh"
        )

        if conexion.is_connected():
            cursor = conexion.cursor()

            # Calcular la fecha límite (hoy - 60 días)
            fecha_limite = datetime.now() - timedelta(days=60)

            # Consulta para eliminar registros
            consulta = f"DELETE FROM {tabla} WHERE fecha < %s"
            valores = (fecha_limite,)

            cursor.execute(consulta, valores)
            conexion.commit()

            cursor.close()
            conexion.close()
    except mysql.connector.Error as err:
        print(f"Error: {err}")


#INICIO DE APP
if __name__ == '__main__':
    app.run(debug=True)