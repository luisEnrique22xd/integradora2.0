from flask import Flask, render_template, request, session, redirect, url_for, Blueprint
from models import db 



app = Flask(__name__, template_folder='inicio/templates' , static_folder='inicio/static' )


admin_bp = Blueprint('admin', __name__, template_folder='administrador/templates')
ayudante_bp = Blueprint('ayudante', __name__, template_folder='ayudante/templates')
app.register_blueprint(admin_bp, url_prefix='/admin')
app.register_blueprint(ayudante_bp, url_prefix='/ayudante')
@app.route('/')
def home():
    return render_template("index.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        tipo_usuario = request.form['tipo_usuario']
        if tipo_usuario == 'Admin':
            # Redireccionar al usuario a la sesión de admin
            return redirect(url_for('sesion_admin'))
        elif tipo_usuario == 'Ayudante':
            # Redireccionar al usuario a la sesión de ayudante
            return redirect(url_for('sesion_ayudante'))
        else:
            # Si el tipo de usuario no es válido, puedes mostrar un mensaje de error o redireccionar a una página de error.
            return render_template('error.html', mensaje='Tipo de usuario no válido')
    else:
        # Renderizar el formulario de inicio de sesión si es una solicitud GET
        return render_template('login.html')

@app.route('/administrador')
def sesion_admin():
    # Lógica para la sesión de administrador
    return render_template('indexad.html')

@app.route('/ayudante')
def sesion_ayudante():
    # Lógica para la sesión de ayudante
    return render_template('indexay.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)

