from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_session import Session
from utils import *
import mysql.connector
from datetime import datetime, timedelta

app = Flask(__name__)
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = True
app.config['SESSION_USE_SIGNER'] = False
app.config['SESSION_KEY_PREFIX'] = 'tu_aplicacion_'
app.secret_key = 'tu_clave_secreta'

Session(app)

"""
RUTAS PARA LOGIN Y LOGOUT
"""

@app.route('/')

def index():
    return render_template('index.html')

#INICIO DE SESION
@app.route('/login', methods = ['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')

    if verificar_credenciales(email, password):
        session['user'] = email
        #registrar_inicio_sesion(email)
        return redirect(url_for('inicio'))
    else:
        return "Credenciales incorrectas"
    
#CIERRE DE SESION   
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))




################################################################################
"""
RUTAS PARA DISTINTAS PAGINAS
"""

#RUTA A AJUSTES
@app.route('/ajustes')
def ajustes():
    if 'user' in session:
        usuario = session['user']
        empleado = obtener_empleado(usuario)
        tupla = obtener_area_jerarquia(usuario)
        jerarquia = tupla[1]

        if jerarquia in ["Direccion", "Gerencia"]:
            return render_template('ajustes.html', usuario=usuario, empleado=empleado, jerarquia=jerarquia)
        else:
            return render_template('ajustes.html', usuario=usuario, empleado=empleado)
    else:
        return redirect(url_for('index'))

#RUTA A AUSENCIAS
@app.route('/ausencias')
def ausencias():
    if 'user' in session:
        usuario = session['user']
        empleado = obtener_empleado(usuario)
        ausencias = obtener_dias_pedidos('ausencias', nombre_empleado=empleado)
        tupla = obtener_area_jerarquia(usuario)
        jerarquia = tupla[1]
        if jerarquia in ["Direccion", "Gerencia"]:
            return render_template('ausencias.html', usuario=usuario, empleado=empleado, ausencias=ausencias, jerarquia=jerarquia)
        else:
            return render_template('ausencias.html', usuario=usuario, empleado=empleado, ausencias=ausencias)
    else:
        return redirect(url_for('index'))
    
#RUTA A EDITAR
@app.route('/editar')
def editar():
    if 'user' in session:
        usuario = session['user']
        empleado = obtener_empleado(usuario)
        tupla = obtener_area_jerarquia(usuario)
        jerarquia = tupla[1]
        area = tupla[0]

        if jerarquia == "Gerencia":
            personal = obtener_personal(area)
            return render_template('editar.html', usuario=usuario, empleado=empleado, personal=personal, jerarquia=jerarquia)
        else:
            personal = obtener_personal()
            return render_template('editar.html', usuario=usuario, empleado=empleado, personal=personal, jerarquia=jerarquia)
    else:
        return redirect(url_for('index'))

#RUTA A ESTUDIO
@app.route('/estudio')
def estudio():
    if 'user' in session:
        usuario = session['user']
        empleado = obtener_empleado(usuario)
        dias_estudio = obtener_dias_pedidos('estudio',area=None, nombre_empleado=empleado)
        tupla = obtener_area_jerarquia(usuario)
        jerarquia = tupla[1]

        if jerarquia in ["Direccion", "Gerencia"]:
            return render_template('estudio.html', usuario=usuario, empleado=empleado, dias_estudio=dias_estudio, jerarquia=jerarquia)
        else:
            return render_template('estudio.html', usuario=usuario, empleado=empleado, dias_estudio=dias_estudio)
    else:
        return redirect(url_for('index'))

#RUTA A HOMEOFFICE
@app.route('/homeoffice')
def homeoffice():
    if 'user' in session:
        usuario = session['user']
        empleado = obtener_empleado(usuario)
        homeoffice = obtener_dias_pedidos('homeoffice', nombre_empleado=empleado)
        tupla = obtener_area_jerarquia(usuario)
        jerarquia = tupla[1]

        if jerarquia in ["Direccion", "Gerencia"]:
            return render_template('homeoffice.html', usuario=usuario, empleado=empleado, homeoffice=homeoffice, jerarquia=jerarquia)
        else:
            return render_template('homeoffice.html', usuario=usuario, empleado=empleado, homeoffice=homeoffice)
    else:
        return redirect(url_for('index'))

#RUTA A INICIO
@app.route('/inicio')
def inicio():
    if 'user' in session:
        usuario = session['user']
        empleado = obtener_empleado(usuario)
        tupla = obtener_area_jerarquia(usuario)
        jerarquia = tupla[1]
        area = tupla[0]

        if jerarquia in ["Direccion", "Gerencia"]:
            estudio = obtener_dias_pedidos('estudio', area=None, nombre_empleado=None)
            ausencias = obtener_dias_pedidos('ausencias', area=None, nombre_empleado=None)
            home = obtener_dias_pedidos('homeoffice', area=None, nombre_empleado=None)
            return render_template('inicio.html', usuario=usuario, empleado=empleado, estudio=estudio, ausencias=ausencias, home=home, jerarquia=jerarquia, area=area)
        else:
            return render_template('inicio.html', usuario=usuario, empleado=empleado)
    else:
        return redirect(url_for('index'))

#RUTA A VACACIONES
@app.route('/vacaciones')
def vacaciones():
    if 'user' in session:
        usuario = session['user']
        empleado = obtener_empleado(usuario)
        vacaciones = obtener_vacaciones(empleado)
        tupla = obtener_area_jerarquia(usuario)
        jerarquia = tupla[1]
        
        if jerarquia in ["Direccion", "Gerencia"]:
            return render_template('vacaciones.html', usuario=usuario, empleado=empleado, vacaciones=vacaciones, jerarquia=jerarquia)
        else:
            return render_template('vacaciones.html', usuario=usuario, empleado=empleado, vacaciones=vacaciones)
    else:
        return redirect(url_for('index'))
    


################################################################################
"""
RUTAS Y FUNCIONES EXTRAS
"""

#GUARDAR FECHA DE ESTUDIO
@app.route('/guardar_estudio', methods=['POST'])
def guardar_fecha_route():
    return guardar_fecha_generico('estudio', 'fechaEstudio')
    
#GUARDAR FECHA DE HOME OFFICE
@app.route('/guardar_home', methods=['POST'])
def guardar_home_route():
    return guardar_fecha_generico('homeoffice', 'fechaHome')

#GUARDAR FECHA DE AUSENCIAS
@app.route('/guardar_ausencias', methods=['POST'])
def guardar_ausencias_route():
    return guardar_fecha_generico('ausencias', 'fechaAusencias')

#GUARDAR FECHA DE VACACIONES
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

#FUNCION PARA GUARDAR FECHA DE FORMA GENERICA PARA SER REUTILIZADA
def guardar_fecha_generico(pagina, campo_fecha):
    if 'user' in session:
        correo = session['user']
        nombre_empleado = obtener_empleado(correo)
        tupla = obtener_area_jerarquia(correo)
        area, jerarquia = tupla
        
        fecha = request.form.get(campo_fecha)

        resultado = guardar_fecha(nombre_empleado, fecha, area, jerarquia, pagina)

        if resultado:
            return redirect(url_for(pagina))
        else:
            return "Error al guardar la fecha"
    else:
        return redirect(url_for('index'))
    
#CAMBIAR LA CONTRASEÑA
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

#ELEGIR USUARIO Y GUARDAR LOS DATOS DEL EMPLEADO
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
                    tupla = obtener_area_jerarquia(usuario)
                    jerarquia = tupla[1]
                    area = tupla[0]

                    if jerarquia == "Gerencia":
                        personal = obtener_personal(area)
                    else:
                        personal = obtener_personal()

                    return render_template('editar.html', usuario=usuario, empleado=empleado, personal=personal, datos=informacion_empleado)
                else:
                    return redirect(url_for('index'))

#GUARDAR LA INFORMACION CAMBIADA A LOS EMPLEADOS
@app.route('/guardar_informacion', methods=['POST'])
def guardar_informacion():
    if request.method == 'POST':
        nombre = request.form.get('empleado')
        cuenta = request.form.get('cuenta')
        forma = request.form.get('forma')
        turno = request.form.get('turno')
        area = request.form.get('area')
        equipo = request.form.get('equipo')
        convenio = request.form.get('convenio')
        legajo = request.form.get('legajo')
        mail = request.form.get('mail')

        exito_actualizacion = actualizar_datos_empleado(nombre, cuenta, forma, turno, area, equipo, convenio, legajo, mail)

        if exito_actualizacion:
            return redirect(url_for('editar'))
        else:
            return redirect(url_for('editar'))
        
#Eliminar empleado
@app.route('/eliminar_empleado', methods=['POST'])
def eliminar_empleado():
    if request.method == 'POST':
        empleado_a_eliminar = request.form.get('empleado')
        if empleado_a_eliminar:
            actualizar_cuenta(empleado_a_eliminar)
            return redirect(url_for('editar'))
        else:
            return "Nombre del empleado no encontrado", 400

#Comentario para eliminar registros de las bases de datos
"""
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
"""





################################################################################
"""
RUTAS Y FUNCIONES PARA CARGAR INFORMACION EN EL CALENDARIO (SOLO PARA RRHH, DIRECCION Y GERENTES)
"""

def obtener_eventos(concepto, area=None):
    dias_eventos = obtener_dias_pedidos(concepto, area=area, nombre_empleado=None)
    
    eventos = []
    
    for tupla in dias_eventos:
        empleado, fecha = tupla
        eventos.append({
            'title': empleado,
            'start': fecha,
            'end': fecha
        })
    
    return eventos

def obtener_eventos_vacaciones(area=None):
    dias_vacaciones = obtener_vacaciones(area=area, nombre_empleado=None)
    eventos = []
    for vacaciones in dias_vacaciones:
        empleado, fecha_inicio, fecha_fin = vacaciones
        eventos.append({
            'title': empleado,
            'start': fecha_inicio,
            'end': fecha_fin
        })
    
    return eventos

def obtener_todos_los_eventos(area=None):
    eventos_estudio = obtener_eventos('estudio', area=area)
    eventos_ausencias = obtener_eventos('ausencias', area=area)
    eventos_home = obtener_eventos('homeoffice', area=area)
    eventos_vacaciones = obtener_eventos_vacaciones(area=area)

    for evento in eventos_estudio:
        evento['color'] = 'blue'
    for evento in eventos_home:
        evento['color'] = 'green'
    for evento in eventos_ausencias:
        evento['color'] = 'red'
    for evento in eventos_vacaciones:
        evento['color'] = 'pink'

    eventos = eventos_estudio + eventos_ausencias + eventos_home + eventos_vacaciones

    return eventos

#Ruta para el calendario general (RRHH y Direccion)
@app.route('/obtener_todos_los_eventos', methods=['GET'])
def obtener_todos_los_eventos_route():
    eventos = obtener_todos_los_eventos()
    return jsonify(eventos)

#Rutas por sector
@app.route('/obtener_todos_los_eventosAccount', methods=['GET'])
def obtener_todos_los_eventosAccount_route():
    eventos = obtener_todos_los_eventos("Account Manager")
    return jsonify(eventos)

@app.route('/obtener_todos_los_eventosAnalytics', methods=['GET'])
def obtener_todos_los_eventosAnalytics_route():
    eventos = obtener_todos_los_eventos("Analytics")
    return jsonify(eventos)

@app.route('/obtener_todos_los_eventosBorderaux', methods=['GET'])
def obtener_todos_los_eventosBorderaux_route():
    eventos = obtener_todos_los_eventos("Borderaux")
    return jsonify(eventos)

@app.route('/obtener_todos_los_eventosComercial', methods=['GET'])
def obtener_todos_los_eventosComercial_route():
    eventos = obtener_todos_los_eventos("Comercial")
    return jsonify(eventos)

@app.route('/obtener_todos_los_eventosClaims', methods=['GET'])
def obtener_todos_los_eventosClaims_route():
    eventos = obtener_todos_los_eventos("Data Claims")
    return jsonify(eventos)

@app.route('/obtener_todos_los_eventosIntegrity', methods=['GET'])
def obtener_todos_los_eventosIntegrity_route():
    eventos = obtener_todos_los_eventos("Data Integrity")
    return jsonify(eventos)

@app.route('/obtener_todos_los_eventosMaestranza', methods=['GET'])
def obtener_todos_los_eventosMaestranza_route():
    eventos = obtener_todos_los_eventos("Maestranza")
    return jsonify(eventos)

@app.route('/obtener_todos_los_eventosOperaciones', methods=['GET'])
def obtener_todos_los_eventosOperaciones_route():
    eventos = obtener_todos_los_eventos("Operaciones")
    return jsonify(eventos)

@app.route('/obtener_todos_los_eventosPagos', methods=['GET'])
def obtener_todos_los_eventosPagos_route():
    eventos = obtener_todos_los_eventos("Pagos")
    return jsonify(eventos)

@app.route('/obtener_todos_los_eventosQuality', methods=['GET'])
def obtener_todos_los_eventosQuality_route():
    eventos = obtener_todos_los_eventos("Quality")
    return jsonify(eventos)

@app.route('/obtener_todos_los_eventosReintegros', methods=['GET'])
def obtener_todos_los_eventosReintegros_route():
    eventos = obtener_todos_los_eventos("Reintegros")
    return jsonify(eventos)

@app.route('/obtener_todos_los_eventosRRHH', methods=['GET'])
def obtener_todos_los_eventosRRHH_route():
    eventos = obtener_todos_los_eventos("RRHH")
    return jsonify(eventos)

@app.route('/obtener_todos_los_eventosSistemas', methods=['GET'])
def obtener_todos_los_eventosSistemas_route():
    eventos = obtener_todos_los_eventos("Sistemas")
    return jsonify(eventos)

################################################################################
#INICIO DE APP
if __name__ == '__main__':
    app.run(debug=True)