from flask import Flask, render_template, request, session, redirect, url_for, Blueprint, flash
import mysql.connector
from models.db import get_connection
usuarios_registrados = []
visitantes_registrados = []


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
@app.route('/')
def home():
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
         cursor.execute('SELECT nombre, ape_pat, ape_Mat, Origen, edad, genero, institucion, fecha_registro FROM visitante')
         visitantes = cursor.fetchall()
         cursor.close()
         return render_template('visitante.html', visitantes=visitantes)
    # Renderiza la plantilla HTML con los resultados

@app.route('/user')
def usuarios():
   cursor = mydb.cursor(dictionary=True)
   cursor.execute('SELECT nombre, apellidos, tipoCargo, nomUsuario,contrasenia FROM usuario')
   usuarios = cursor.fetchall()
   cursor.close()
   return render_template('user.html', usuarios=usuarios)
    # Renderiza la plantilla HTML con los resultados


if __name__ == '__main__':
    app.run(debug=True, port=5000)

