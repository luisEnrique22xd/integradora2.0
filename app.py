from flask import Flask, render_template, request, session, redirect, url_for, Blueprint, flash, jsonify
import mysql.connector
import os 
from models.db import get_connection
usuarios_registrados = []
visitantes_registrados = []
items_registrados = []
visitas=[]


app = Flask(__name__, template_folder='inicio/templates' , static_folder='inicio/static' )
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
        cursor = mydb.cursor()
        sql = "SELECT * FROM usuario WHERE nomUsuario = %s"
        cursor.execute(sql, (username,))
        user_data = cursor.fetchone()
        cursor.close()
        mydb.close()

        if user_data and user_data['contrasenia'] == password:
            return True
        return False

    except Exception as e:
        print("Error al verificar las credenciales:", str(e))
        return False
    
@app.route('/login', methods=['GET', 'POST'])
def login():
       if request.method == 'POST':
        tipoCargo = request.form['tipoCargo']
        if tipoCargo == 'Administrador':
            # Redireccionar al usuario a la sesión de admin
            return redirect(url_for('Administrador'))
        elif tipoCargo == 'Ayudante':
            # Redireccionar al usuario a la sesión de ayudante
            return redirect(url_for('Ayudante'))
        flash('Tipo de usuario no válido. Por favor, verifica tus datos' , 'error')
        return redirect(url_for('login'))  # Redirigir al formulario de inicio de sesión nuevamente.

       else:
        # Renderizar el formulario de inicio de sesión si es una solicitud GET
        return render_template('login.html')

@app.route('/Administrador')
def Administrador():
    # Lógica para la sesión de administrador
    return render_template('indexad.html')

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
    return render_template('indexay.html')

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


if __name__ == '__main__':
    app.run(debug=True, port=5000)

