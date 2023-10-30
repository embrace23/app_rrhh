from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
from flask_session import Session
from utils import *
import mysql.connector
from datetime import datetime, timedelta
from notifypy import Notify

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
        flash('Credenciales incorrectas.', 'success')
        return redirect(url_for('inicio'))
    
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
        ausencias_notificadas = obtener_dias_pedidos('ausencias', nombre_empleado=empleado, aprobado="SI")
        ausencias_por_notificar = obtener_dias_pedidos('ausencias', nombre_empleado=empleado, aprobado="NO")
        tupla = obtener_area_jerarquia(usuario)
        jerarquia = tupla[1]
        if jerarquia in ["Direccion", "Gerencia"]:
            return render_template('ausencias.html', usuario=usuario, empleado=empleado, ausencias_notificadas=ausencias_notificadas, ausencias_por_notificar=ausencias_por_notificar, jerarquia=jerarquia)
        else:
            return render_template('ausencias.html', usuario=usuario, empleado=empleado, ausencias_notificadas=ausencias_notificadas, ausencias_por_notificar=ausencias_por_notificar)
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
        dias_estudio_aprobados = obtener_dias_pedidos('estudio',area=None, nombre_empleado=empleado, aprobado="SI")
        dias_estudio_en_espera = obtener_dias_pedidos('estudio',area=None, nombre_empleado=empleado, aprobado="NO")
        tupla = obtener_area_jerarquia(usuario)
        jerarquia = tupla[1]

        if jerarquia in ["Direccion", "Gerencia"]:
            return render_template('estudio.html', usuario=usuario, empleado=empleado, dias_aprobados=dias_estudio_aprobados, dias_espera=dias_estudio_en_espera, jerarquia=jerarquia)
        else:
            return render_template('estudio.html', usuario=usuario, empleado=empleado, dias_aprobados=dias_estudio_aprobados, dias_espera=dias_estudio_en_espera)
    else:
        return redirect(url_for('index'))

#RUTA A HOMEOFFICE
@app.route('/homeoffice')
def homeoffice():
    if 'user' in session:
        usuario = session['user']
        empleado = obtener_empleado(usuario)
        homeoffice_notificados = obtener_dias_pedidos('homeoffice', nombre_empleado=empleado, aprobado="SI")
        homeoffice_en_espera = obtener_dias_pedidos('homeoffice', nombre_empleado=empleado, aprobado="NO")
        tupla = obtener_area_jerarquia(usuario)
        jerarquia = tupla[1]

        if jerarquia in ["Direccion", "Gerencia"]:
            return render_template('homeoffice.html', usuario=usuario, empleado=empleado, homeoffice_notificados=homeoffice_notificados, homeoffice_en_espera=homeoffice_en_espera, jerarquia=jerarquia)
        else:
            return render_template('homeoffice.html', usuario=usuario, empleado=empleado, homeoffice_notificados=homeoffice_notificados,  homeoffice_en_espera=homeoffice_en_espera)
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
            if jerarquia == "Gerencia":
                dias_para_autorizar = dias_por_autorizar(area)
                vacaciones_autorizar = vacaciones_por_autorizar(area)
            else:
                dias_para_autorizar = dias_por_autorizar()
                vacaciones_autorizar = vacaciones_por_autorizar()
            return render_template('inicio.html', usuario=usuario, empleado=empleado, estudio=estudio, ausencias=ausencias, home=home, jerarquia=jerarquia, area=area, dias_autorizar=dias_para_autorizar, vacaciones_autorizar=vacaciones_autorizar)
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
        vacaciones = obtener_vacaciones(nombre_empleado=empleado)
        tupla = obtener_area_jerarquia(usuario)
        jerarquia = tupla[1]
        area = tupla[0]
        
        if jerarquia in ["Direccion", "Gerencia"]:
            return render_template('vacaciones.html', usuario=usuario, empleado=empleado, vacaciones=vacaciones, jerarquia=jerarquia, area=area)
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
    flash('Se ha solicitado el día de estudio correctamente, el mismo quedará en espera de ser aprobado por su superior inmediato.', 'success')
    return guardar_fecha_generico('estudio', 'fechaEstudio')
    
#GUARDAR FECHA DE HOME OFFICE
@app.route('/guardar_home', methods=['POST'])
def guardar_home_route():
    flash('Se ha informado el día de home office correctamente, el mismo quedará en espera de ser notificado a su superior inmediato.', 'success')
    return guardar_fecha_generico('homeoffice', 'fechaHome')

#GUARDAR FECHA DE AUSENCIAS
@app.route('/guardar_ausencias', methods=['POST'])
def guardar_ausencias_route():
    flash('Se ha guardado la fecha de ausencias correctamente, la misma quedará en espera de ser notificada a su superior inmediato.', 'success')
    return guardar_fecha_generico('ausencias', 'fechaAusencias')

#GUARDAR FECHA DE VACACIONES
@app.route('/guardar_vacaciones', methods=['POST'])
def guardar_vacaciones():
    if 'user' in session:
        correo = session['user']
        nombre_empleado = obtener_empleado(correo)
        tupla = obtener_area_jerarquia(correo)
        area = tupla[0]
        
        fecha_inicio = request.form.get('fecha_inicio')
        fecha_fin = request.form.get('fecha_fin')

        if fecha_inicio and fecha_fin:
            tabla = 'vacaciones'

            fecha_modificacion = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            mensaje = f"{nombre_empleado} solicitó {fecha_inicio} al {fecha_fin}"
            notificacion = Notify()
            notificacion.title = f"Vacaciones"
            notificacion.message = mensaje
            notificacion.send()
            
            campos = {
                'empleado': nombre_empleado,
                'fecha_inicio': fecha_inicio,
                'fecha_fin': fecha_fin,
                'fecha_modificacion': fecha_modificacion,
                'area': area,
                'aprobado': "NO"
            }
            resultado = insertar_registro(tabla, campos)

            if resultado:
                flash('Se han solicitado los días de vacaciones correctamente, la solicitud quedará en espera de ser aprobada por su superior inmediato.', 'success')
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
        mensaje = f"{nombre_empleado} solicitó {fecha}"
        notificacion = Notify()
        notificacion.title = f"{pagina}"
        notificacion.message = mensaje
        notificacion.send()
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
                        flash('Los ajustes se han guardado con éxito', 'success')
                        return redirect(url_for('ajustes'))
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
@app.route('/elegir_empleado', methods=['POST'])
def elegir_empleado():
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

                    return render_template('editar.html', usuario=usuario, empleado=empleado, personal=personal, datos=informacion_empleado, jerarquia=jerarquia)
                else:
                    return redirect(url_for('index'))

#GUARDAR LA INFORMACION CAMBIADA A LOS EMPLEADOS
@app.route('/guardar_informacion', methods=['POST'])
def guardar_informacion():
    if request.method == 'POST':
        empleado = request.form.get('empleado')
        legajo = request.form.get('legajo')
        mail = request.form.get('mail')
        forma = request.form.get('forma')
        turno = request.form.get('turno')
        area = request.form.get('area')
        jerarquia = request.form.get('jerarquia')
        equipo = request.form.get('equipo')
        convenio = request.form.get('convenio')

        exito_actualizacion = actualizar_datos_empleado(empleado, legajo, mail, forma, turno, area, jerarquia, equipo, convenio)

        if exito_actualizacion:
            flash('Los ajustes se han guardado con éxito', 'success')
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
            flash('Se ha eliminado al empleado correctamente.', 'success')
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

#Funcion para aprobar la solicitud del personal
@app.route('/aprobar_solicitud', methods=['POST'])
def aprobar_solicitud_route():
    if request.method == 'POST':
        empleado = request.form.get('empleado')
        fecha = request.form.get('fecha')
        concepto = request.form.get('concepto')
        jerarquia = request.form.get('jerarquia')
        
        if empleado and fecha:
            aprobar_solicitud(empleado, fecha, concepto, jerarquia)
            return redirect(url_for('inicio'))
        else:
            return redirect(url_for('inicio'))
    else:
        return "Método no permitido"

#Funcion para eliminar la solicitud del personal
@app.route('/eliminar_solicitud', methods=['POST'])
def eliminar_solicitud_route():
    if request.method == 'POST':
        empleado = request.form.get('empleado')
        fecha = request.form.get('fecha')
        concepto = request.form.get('concepto')
        
        if empleado and fecha:
            eliminar_solicitud(empleado, fecha, concepto)
            return redirect(url_for('inicio'))
        else:
            return redirect(url_for('inicio'))
    else:
        return "Método no permitido"
    
@app.route('/agregar_home_empleado', methods=['POST'])
def agregar_home_empleado():
    if request.method == 'POST': 
        empleado = request.form.get('empleadoHome')
        fecha = request.form.get('fechaHome')
        area = request.form.get('areaHome')
        jerarquia = request.form.get('jerarquiaHome')
        concepto = 'homeoffice'
        aprobado = "SI"

        resultado = guardar_fecha(empleado, fecha, area, jerarquia, concepto, aprobado)

        if resultado:
            flash('Se ha guardado la fecha de home office correctamente.', 'success')
            return redirect(url_for('editar'))
        else:
            return "Error al guardar la fecha"
    else:
        return redirect(url_for('index'))

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


notificacion = Notify()
notificacion.title = "Titulo"
notificacion.message = "Hola"
notificacion.send()