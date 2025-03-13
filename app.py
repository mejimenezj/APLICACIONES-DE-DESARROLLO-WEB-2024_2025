# app.py
from flask import Flask, render_template, redirect, url_for, flash, request
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
import json
import csv
import os

# Crear la aplicación Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = 'tu_clave_secreta_aqui'  # Necesario para CSRF

# Configuración de SQLAlchemy
basedir = os.path.abspath(os.path.dirname(__file__))  # Ruta base del proyecto
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'database', 'usuarios.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializar SQLAlchemy
db = SQLAlchemy(app)

# Definir el modelo de la tabla `usuarios`
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    edad = db.Column(db.Integer, nullable=False)
    ciudad = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"Usuario('{self.nombre}', {self.edad}, '{self.ciudad}')"

# Definir el formulario
class MiFormulario(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired()])  # Campo de nombre
    edad = IntegerField('Edad', validators=[DataRequired()])  # Campo de edad
    ciudad = StringField('Ciudad', validators=[DataRequired()])  # Campo de ciudad
    submit = SubmitField('Enviar')  # Botón de enviar

# Ruta principal
@app.route("/")
def index():
    return render_template("index.html")

# Ruta para el formulario
@app.route('/formulario', methods=['GET', 'POST'])
def formulario():
    form = MiFormulario()  # Crear una instancia del formulario

    if form.validate_on_submit():  # Validar el formulario al enviar
        nombre = form.nombre.data  # Obtener el nombre
        edad = form.edad.data  # Obtener la edad
        ciudad = form.ciudad.data  # Obtener la ciudad

        # Guardar en TXT
        with open('datos/datos.txt', 'a') as file:
            file.write(f"{nombre},{edad},{ciudad}\n")

        # Guardar en JSON
        with open('datos/datos.json', 'a') as file:
            json.dump({'nombre': nombre, 'edad': edad, 'ciudad': ciudad}, file)
            file.write('\n')  # Agrega un salto de línea para separar entradas

        # Guardar en CSV
        with open('datos/datos.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([nombre, edad, ciudad])

        # Guardar en la base de datos
        nuevo_usuario = Usuario(nombre=nombre, edad=edad, ciudad=ciudad)
        db.session.add(nuevo_usuario)
        db.session.commit()

        flash(f'¡Formulario enviado correctamente, {nombre}!', 'success')  # Mensaje flash
        return redirect(url_for('formulario'))  # Redirigir a la misma página

    return render_template('formulario.html', form=form)  # Renderizar el formulario

# Ruta para leer datos desde un archivo TXT
@app.route('/leer_txt')
def leer_txt():
    try:
        with open('datos/datos.txt', 'r') as file:
            datos = file.readlines()  # Lee todas las líneas del archivo TXT
        return '<br>'.join(datos)  # Muestra los datos en el navegador
    except FileNotFoundError:
        return "El archivo TXT está vacío."

# Ruta para leer datos desde un archivo JSON
@app.route('/leer_json')
def leer_json():
    try:
        with open('datos/datos.json', 'r') as file:
            datos = [json.loads(line) for line in file]  # Lee cada línea como un objeto JSON
        return '<br>'.join([f"{d['nombre']}, {d['edad']}, {d['ciudad']}" for d in datos])  # Muestra los datos en el navegador
    except FileNotFoundError:
        return "El archivo JSON está vacío."
    except json.JSONDecodeError:
        return "El archivo JSON está vacío o mal formateado."

# Ruta para leer datos desde un archivo CSV
@app.route('/leer_csv')
def leer_csv():
    try:
        with open('datos/datos.csv', 'r') as file:
            reader = csv.reader(file)
            datos = [f"{row[0]}, {row[1]}, {row[2]}" for row in reader]  # Lee cada fila del CSV
        return '<br>'.join(datos)  # Muestra los datos en el navegador
    except FileNotFoundError:
        return "El archivo CSV está vacío."

# Ruta para leer datos desde la base de datos
@app.route('/leer_db')
def leer_db():
    usuarios = Usuario.query.all()  # Obtener todos los usuarios
    resultado = "<br>".join([f"ID: {u.id}, Nombre: {u.nombre}, Edad: {u.edad}, Ciudad: {u.ciudad}" for u in usuarios])
    return resultado

# Ruta para la página "about"
@app.route('/about')
def about():
    return render_template('about.html')

# Crear la base de datos y la tabla (solo la primera vez)
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)