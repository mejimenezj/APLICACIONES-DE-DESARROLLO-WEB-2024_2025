from flask import Flask, render_template, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'tu_clave_secreta_aqui'  # Necesario para CSRF

# Definir el formulario
class MiFormulario(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired()])  # Campo de nombre
    submit = SubmitField('Enviar')  # Botón de enviar

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/home")
def home():
    return render_template("index.html")

@app.route('/about')
def about():
    return render_template("about.html")

# Ruta para el formulario
@app.route('/formulario', methods=['GET', 'POST'])
def formulario():
    form = MiFormulario()  # Crear una instancia del formulario

    if form.validate_on_submit():  # Validar el formulario al enviar
        nombre = form.nombre.data  # Obtener el dato del campo "nombre"
        flash(f'¡Formulario enviado correctamente, {nombre}!', 'success')  # Mensaje flash
        return redirect(url_for('formulario'))  # Redirigir a la misma página

    return render_template('formulario.html', form=form)  # Renderizar el formulario

if __name__ == "__main__":
    app.run(debug=True)