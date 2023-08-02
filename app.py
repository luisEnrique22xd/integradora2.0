from flask import Flask, render_template, request, session, redirect, url_for, Blueprint, flash, jsonify
import mysql.connector
import os 
import time
from models.db import get_connection
usuarios_registrados = []
visitantes_registrados = []
items_registrados = []
visitas=[]


app = Flask(__name__, template_folder='inicio/templates' , static_folder='inicio/static' )
app.secret_key= ''
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="scamch",
)

admin_bp = Blueprint('admin', __name__, template_folder='administrador/templates')
ayudante_bp = Blueprint('ayudante', __name__, template_folder='ayudante/templates')
app.register_blueprint(admin_bp, url_prefix='/admin')
app.register_blueprint(ayudante_bp, url_prefix='/ayudante')
app.secret_key = os.urandom(24)

@app.route('/inicio', endpoint='inicio.index')
def inicio():
    return render_template("index.html")


@app.route("/registro", methods=['GET','POST'])

def registro():
    if request.method == 'POST':
        # Obtener los datos enviados desde el formulario
        if 'tipoCargo' not in request.form:
            return "Campo 'tipoCargo' no encontrado en el formulario."

        nombre = request.form['nombre']
        apellidos = request.form['apellidos']
        tipoCargo = request.form['tipoCargo']
        nomUsuario = request.form['nomUsuario']
        password = request.form['password']

        try:
            # Obtener la conexión a la base de datos
            mydb = get_connection()
            cursor = mydb.cursor()

            # Consulta SQL para insertar los datos en la tabla de usuarios
            sql = "INSERT INTO usuario (nombre, apellidos, tipoCargo, nomUsuario, contrasenia) VALUES (%s, %s, %s, %s, %s)"
            val = (nombre, apellidos, tipoCargo, nomUsuario, password)

            # Ejecutar la consulta SQL
            cursor.execute(sql, val)

            # Confirmar los cambios en la base de datos
            mydb.commit()

            # Cerrar el cursor y la conexión a la base de datos
            cursor.close()
            mydb.close()

            # Redireccionar a la página de inicio después de registrar al usuario
            return redirect(url_for('login'))

        except Exception as e:
            # Si ocurre algún error, imprimirlo en la consola y mostrar un mensaje de error al usuario
            print("Error al insertar datos en la base de datos:", str(e))
            return render_template('error.html', mensaje='Error al registrar al usuario')

    else:
        # Mostrar el formulario de registro
        return render_template('registro.html')
    

def verificar_credenciales(username, password):
    try:
        mydb = get_connection()
        cursor = mydb.cursor(dictionary=True)
        sql = f"SELECT * FROM usuario WHERE nomUsuario = '{username}'"
        cursor.execute(sql)
        user_data = cursor.fetchone()
        cursor.close()
        mydb.close()

        if user_data and user_data['contrasenia'] == password:
            return user_data
        return False

    except Exception as e:
        print("Error al verificar las credenciales:", str(e))
        return False
    
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        #tipoCargo = request.form['tipoCargo']
        user_valid = verificar_credenciales(request.form['nomUsuario'], request.form['password'])
        if user_valid == False:
            flash('Tipo de usuario no válido. Por favor, verifica tus datos' , 'error')
            return redirect(url_for('login'))  # Redirigir al formulario de inicio de sesión nuevamente.    
        if user_valid['tipoCargo'] == 'Administrador':
            # Redireccionar al usuario a la sesión de admin
            session['usuario'] = user_valid
            return redirect(url_for('Administrador'))
        elif user_valid['tipoCargo'] == 'Ayudante':
            # Redireccionar al usuario a la sesión de ayudante
            session['usuario'] = user_valid
            return redirect(url_for('Ayudante'))
        #flash('Tipo de usuario no válido. Por favor, verifica tus datos' , 'error')
        #return redirect(url_for('login'))  # Redirigir al formulario de inicio de sesión nuevamente.

    else:
        # Renderizar el formulario de inicio de sesión si es una solicitud GET
        return render_template('login.html')

@app.route('/Administrador') 
def Administrador():
    # Lógica para la sesión de administrador
    if session['usuario']['tipoCargo'] == 'Administrador':
        return render_template('indexad.html')
    else:
        return redirect (url_for('Ayudante'))

@app.route("/registrarItem", methods=['GET','POST'])
def registrarItem():
    if request.method == 'POST':
        # Obtener los datos enviados desde el formulario
        print(request.form)

        nombre = request.form['nombre']
        origen = request.form['origen']
        modAdqui = request.form['modAdqui']
        fecha_registro = request.form['fecha_registro']
        categoria = request.form['categoria']
        temporada= request.form['temporada']
        condicion= request.form['condicion']

        try:
            # Obtener la conexión a la base de datos
            mydb = get_connection()
            cursor = mydb.cursor()

            # Consulta SQL para insertar los datos en la tabla de usuarios
            sql = "INSERT INTO item (nombre, origen, modAdqui, fecha_registro, categoria, temporada, condicion) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            val = (nombre, origen, modAdqui, fecha_registro, categoria, temporada, condicion)

            # Ejecutar la consulta SQL
            cursor.execute(sql, val)

            # Confirmar los cambios en la base de datos
            mydb.commit()

            # Cerrar el cursor y la conexión a la base de datos
            cursor.close()
            mydb.close()

            # Redireccionar a la página de inicio después de registrar al usuario
            return redirect(url_for('registrarItem'))

        except Exception as e:
            # Si ocurre algún error, imprimirlo en la consola y mostrar un mensaje de error al usuario
            print("Error al insertar datos en la base de datos:", str(e))
            return render_template('error.html', mensaje='Error al registrar al usuario')

    else:
        # Mostrar el formulario de registro
        # Consultar origenitem
        mydb = get_connection()
        cursor = mydb.cursor(dictionary=True )
        sql = ('SELECT * FROM origenitem')
        cursor.execute(sql)
        origenes=cursor.fetchall()
        #mydb.commit()
        #modos de adquisicion
        sql1= ('SELECT * FROM modadqui')
        cursor.execute(sql1)
        modosadqui=cursor.fetchall()
        # categorias
        sql2= ('SELECT * FROM categoria')
        cursor.execute(sql2)
        categorias=cursor.fetchall()
        #temporadas
        sql3=('SELECT * FROM temporada')
        cursor.execute(sql3)
        temporadas=cursor.fetchall()
        cursor.close()
        mydb.close()
        return render_template('registrarItem.html',origenes=origenes, modosadqui=modosadqui, categorias= categorias, temporadas=temporadas)

@app.route("/registrarOrigen", methods=['GET','POST'])
def registrarOrigen():     
         
    if request.method == 'POST':
        # Obtener los datos enviados desde el formulario


        lugar = request.form['lugar']

        try:
            # Obtener la conexión a la base de datos
            mydb = get_connection()
            cursor = mydb.cursor()

            # Consulta SQL para insertar los datos en la tabla de usuarios
            sql = "INSERT INTO origenitem (lugar) VALUES (%s)"
            val = (lugar,)

            # Ejecutar la consulta SQL
            cursor.execute(sql, val)

            # Confirmar los cambios en la base de datos
            mydb.commit()

            # Cerrar el cursor y la conexión a la base de datos
            cursor.close()
            mydb.close()
            print(val)
            # Redireccionar a la página de inicio después de registrar al usuario
            return redirect(url_for('registrarOrigen'))

        except Exception as e:
            # Si ocurre algún error, imprimirlo en la consola y mostrar un mensaje de error al usuario
            print("Error al insertar datos en la base de datos:", str(e))
            return render_template('error.html', mensaje='Error al registrar al origen')
    return render_template('registrarItem.html')     
        
@app.route("/registrarCategoria", methods=['GET','POST'])
def registrarCategoria():     
         
        if request.method == 'POST':
        # Obtener los datos enviados desde el formulario


            nombre_cat = request.form['nombre_cat']

            try:
                # Obtener la conexión a la base de datos
                mydb = get_connection()
                cursor = mydb.cursor()

                # Consulta SQL para insertar los datos en la tabla de usuarios
                sql = "INSERT INTO categoria (nombre_cat) VALUES (%s)"
                val = (nombre_cat,)

                # Ejecutar la consulta SQL
                cursor.execute(sql, val)

                # Confirmar los cambios en la base de datos
                mydb.commit()

                # Cerrar el cursor y la conexión a la base de datos
                cursor.close()
                mydb.close()
                print(val)
                # Redireccionar a la página de inicio después de registrar al usuario
                return redirect(url_for('registrarCategoria'))

            except Exception as e:
                # Si ocurre algún error, imprimirlo en la consola y mostrar un mensaje de error al usuario
                print("Error al insertar datos en la base de datos:", str(e))
                return render_template('error.html', mensaje='Error al registrar la categoria')
        return render_template('registrarItem.html')
            
@app.route("/registrarTemporada", methods=['GET','POST'])
def registrarTemporada():     
        if request.method == 'POST':
        
            nombreTemp = request.form['nombreTemp']
            fecha_inicio = request.form['fecha_inicio']
            fecha_final = request.form['fecha_final']


            try:
            # Obtener la conexión a la base de datos
                mydb = get_connection()
                cursor = mydb.cursor()

            # Consulta SQL para insertar los datos en la tabla de usuarios
                sql = "INSERT INTO temporada (nombreTemp ,fecha_inicio, fecha_final) VALUES (%s,%s,%s)"
                val = (nombreTemp, fecha_inicio, fecha_final)

            # Ejecutar la consulta SQL
                cursor.execute(sql, val)

            # Confirmar los cambios en la base de datos
                mydb.commit()

            # Cerrar el cursor y la conexión a la base de datos
                cursor.close()
                mydb.close()
                print(val)
                # Redireccionar a la página de inicio después de registrar al usuario
                return redirect(url_for('registrarTemporada'))

            except Exception as e:
                # Si ocurre algún error, imprimirlo en la consola y mostrar un mensaje de error al usuario
                print("Error al insertar datos en la base de datos:", str(e))
            return render_template('error.html', mensaje='Error al registrar la temporada')
        
        return render_template('registrarItem.html')
@app.route('/item')
def item():
        try: 
          mydb = get_connection()
          cursor = mydb.cursor(dictionary=True)
          cursor.execute('SELECT item.nombre, origenitem.lugar, modadqui.modo, item.fecha_registro,categoria.nombre_cat, temporada.nombreTemp, item.condicion FROM item INNER JOIN modadqui ON item.modAdqui = modadqui.Adqui  INNER JOIN categoria ON item.categoria = categoria.categoria INNER JOIN origenitem ON item.origen = origenitem.id_origen INNER JOIN temporada ON item.temporada = temporada.temporada;')
          items = cursor.fetchall()
          print(items)
          return render_template('item.html', items=items)
    # Renderiza la plantilla HTML con los resultados
        except Exception as e:
         print("Error al obtener los items:", str(e))
        return render_template('error.html', mensaje='Error al obtener los items')

@app.route('/Ayudante')
def Ayudante():
    # Lógica para la sesión de ayudante
    if session['usuario']['tipoCargo'] == 'Ayudante':
        return render_template('indexay.html')
    else:
        return redirect (url_for('Administrador'))

@app.route("/registroVisitante", methods=['GET','POST'])

def registroVisitante():
    if request.method == 'POST':
        # Obtener los datos enviados desde el formulario

        nombre = request.form['nombre']
        ape_pat = request.form['ape_pat']
        ape_Mat = request.form['ape_Mat']
        Origen = request.form['Origen']
        edad = request.form['edad']
        genero= request.form['genero']
        institucion= request.form['institucion']
        fecha_registro= request.form['fecha_registro']

        

        try:
            # Obtener la conexión a la base de datos
            mydb = get_connection()
            cursor = mydb.cursor()

            # Consulta SQL para insertar los datos en la tabla de usuarios
            sql = "INSERT INTO visitante (nombre, ape_pat, ape_Mat, Origen, edad, genero, institucion, fecha_registro) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            val = (nombre, ape_pat, ape_Mat, Origen, edad, genero, institucion, fecha_registro)

            # Ejecutar la consulta SQL
            cursor.execute(sql, val)

            # Confirmar los cambios en la base de datos
            mydb.commit()

            # Cerrar el cursor y la conexión a la base de datos
            cursor.close()
            mydb.close()

            # Redireccionar a la página de inicio después de registrar al usuario
            return redirect(url_for('registroVisitante'))

        except Exception as e:
            # Si ocurre algún error, imprimirlo en la consola y mostrar un mensaje de error al usuario
            print("Error al insertar datos en la base de datos:", str(e))
            return render_template('error.html', mensaje='Error al registrar al usuario')

    else:
        # Mostrar el formulario de registro
        return render_template('registroVisitante.html')
    
@app.route('/visitante')
def visitante():
         mydb = get_connection()
         cursor = mydb.cursor(dictionary=True)
         cursor = mydb.cursor(dictionary=True)
         cursor.execute('SELECT id_visitante, nombre, ape_pat, ape_Mat, Origen, edad, genero, institucion, fecha_registro FROM visitante')
         visitantes = cursor.fetchall()
         cursor.close()
         return render_template('visitante.html', visitantes=visitantes)
    # Renderiza la plantilla HTML con los resultados

@app.route("/registroVisitas", methods= ['GET','POST'])
def registroVisitas():
        # Obtener los datos enviados desde el formulario

    if request.method == 'POST':
        # Obtener los datos enviados desde el formulario
         id_visitante = request.form['id_visitante']
         cantidad_visitante = request.form['cantidad_visitante']
         fecha_visita = request.form['fecha_visita']
         tipo_visita = request.form['tipo_visita']
        

        
            # Obtener la conexión a la base de datos
         mydb = get_connection()
         cursor = mydb.cursor()

            # Consulta SQL para insertar los datos en la tabla de usuarios
         sql = "INSERT INTO visitas (id_visitante, cantidad_visitante, fecha_visita, tipo_visita) VALUES (%s, %s, %s, %s)"
         val = (id_visitante, cantidad_visitante, fecha_visita, tipo_visita)

            # Ejecutar la consulta SQL
         cursor.execute(sql, val)

            # Confirmar los cambios en la base de datos
         mydb.commit()

            # Cerrar el cursor y la conexión a la base de datos
         cursor.close()
         mydb.close()

            # Redireccionar a la página de inicio después de registrar al usuario
         return redirect(url_for('registroVisitas'))

    else:
        # Mostrar el formulario de registro
        return render_template('registroVisitas.html')

@app.route("/visitas")
def visitas():
    try:        
        mydb = get_connection()
        cursor = mydb.cursor(dictionary=True)
        cursor = mydb.cursor(dictionary=True)
        cursor.execute('SELECT vs.id_visita AS "ID", CONCAT (v.ape_pat," ", v.ape_Mat," ", v.nombre) AS "Nombre Completo", vs.cantidad_visitante AS "Numero de visitantes", vs.fecha_visita AS "Fecha de Visita", vs.tipo_visita AS "Tipo de visita" FROM visitas AS vs INNER JOIN visitante AS v ON vs.id_visitante = v.id_visitante ')
        visitas = cursor.fetchall()
        cursor.close()
        return render_template('visitas.html', visitas=visitas)
    except mysql.connector.Error as err:
        print ("error en la consulta:", err)

@app.route("/editarVisitante")
def editarVisitante():
    return render_template('editarVisitante.html')

@app.route('/usuario')
def usuario():
   cursor = mydb.cursor(dictionary=True)
   cursor.execute('SELECT nombre, apellidos, tipoCargo, nomUsuario,contrasenia FROM usuario')
   usuarios = cursor.fetchall()
   cursor.close()
   return render_template('user.html', usuario=usuarios)
    # Renderiza la plantilla HTML con los resultados
    # cambie el usuario= usuarios 
@app.route("/buscarUsuario", methods=['GET', 'POST'])
def buscarUsuario():
    if request.method == "POST":
        search = request.form['buscar']
        mydb= get_connection()
        cursor = mydb.cursor(dictionary=True)
        cursor.execute("SELECT * FROM usuario WHERE nombre LIKE %s ORDER BY idUsuario DESC",('%'+search+'%',))
        busqueda = cursor.fetchone()
        cursor.close()
        mydb.close()
        if not busqueda:
            busqueda= None
            busqueda={'mensaje:' 'No se encontraron resultados para la busqueda'}
    return render_template('buscarUser.html', miData = busqueda, busqueda = search)


if __name__ == '__main__':
    app.run(debug=True, port=5000)

