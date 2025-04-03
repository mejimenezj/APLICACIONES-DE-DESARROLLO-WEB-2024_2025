from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models.models import Usuario
from Conexion.conexion import obtener_conexion
from decimal import Decimal
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mi_secreto_seguro'

# Configuración de Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(id_usuario):
    return Usuario.obtener_por_id(id_usuario)

# Clase de formulario existente
class NombreForm(FlaskForm):
    nombre = StringField('Ingresa tu nombre', validators=[DataRequired(), Length(min=2, max=50)])
    submit = SubmitField('Enviar')


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/formulario', methods=['GET', 'POST'])
def formulario():
    form = NombreForm()
    if form.validate_on_submit():
        session['nombre'] = form.nombre.data
        flash('Formulario enviado con éxito!', 'success')
        return redirect(url_for('resultado'))
    return render_template('formulario.html', form=form)

@app.route('/resultado')
def resultado():
    nombre = session.get('nombre', None)
    if nombre is None:
        flash('No hay datos en la sesión. Ingresa tu nombre en el formulario.', 'warning')
        return redirect(url_for('formulario'))
    return render_template('resultado.html', nombre=nombre)

@app.route('/test_db')
def test_db():
    conexion = obtener_conexion()
    if conexion:
        return "Conexión exitosa a MySQL"
    else:
        return "Error en la conexión a MySQL"

# RUTAS DE AUTENTICACIÓN
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Validación básica de campos
        if not email or not password:
            flash('Todos los campos son obligatorios', 'danger')
            return redirect(url_for('login'))
        
        usuario = Usuario.obtener_por_email(email)
        
        if not usuario:
            flash('Email no registrado', 'danger')
            return redirect(url_for('login'))
            
        if not check_password_hash(usuario.password, password):
            flash('Contraseña incorrecta', 'danger')
            return redirect(url_for('login'))
            
        login_user(usuario)
        flash(f'Bienvenido {usuario.nombre}! Has iniciado sesión correctamente', 'success')
        return redirect(url_for('index')) 
        
    return render_template('login.html')

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        email = request.form.get('email')
        nombre = request.form.get('nombre')
        password = request.form.get('password')
        
        if not all([email, nombre, password]):
            flash('Todos los campos son obligatorios', 'danger')
            return redirect(url_for('registro'))
        
        usuario_existente = Usuario.obtener_por_email(email)
        if usuario_existente:
            flash('Este email ya está registrado', 'danger')
            return redirect(url_for('registro'))
        
        try:
            password_hash = generate_password_hash(password)
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute(
                "INSERT INTO usuarios (nombre, email, password) VALUES (%s, %s, %s)",
                (nombre, email, password_hash)
            )
            conexion.commit()
            flash('Registro exitoso. Ahora puedes iniciar sesión', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            flash(f'Error al registrar: {str(e)}', 'danger')
        finally:
            if conexion.is_connected():
                cursor.close()
                conexion.close()
    
    return render_template('registro.html')
# Ruta para obtener todos los usuarios de la base de datos

@app.route('/usuarios_formulario', methods=['GET'])
def obtener_usuarios():
    conexion = obtener_conexion()
    if conexion:
        cursor = conexion.cursor(dictionary=True)  # Para obtener los resultados en formato de diccionario
        cursor.execute("SELECT * FROM usuarios")
        usuarios = cursor.fetchall()
        cursor.close()
        conexion.close()
        return jsonify(usuarios)  # Retornar los datos en formato JSON
    else:
        return jsonify({"error": "No se pudo conectar a la base de datos"}), 500

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Has cerrado sesión correctamente', 'success')
    return redirect(url_for('login')) 


# RUTAS DE PRODUCTOS

@app.route('/productos')
# @login_required
def productos():
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("SELECT * FROM productos")
        productos = cursor.fetchall()
        return render_template('productos.html', productos=productos)
    except Exception as e:
        flash(f'Error al cargar productos: {str(e)}', 'error')
        return render_template('productos.html', productos=[])
    finally:
        if 'conexion' in locals() and conexion.is_connected():
            conexion.close()

@app.route('/crear_productos', methods=['GET', 'POST'])
#@login_required
def crear_productos():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        precio = request.form.get('precio')
        stock = request.form.get('stock')
        
        if not all([nombre, precio, stock]):
            flash("Todos los campos son obligatorios", "danger")
            return redirect(url_for('crear_productos'))
        
        try:
            precio = Decimal(precio)
            stock = int(stock)
        except:
            flash("Precio y stock deben ser valores numéricos", "danger")
            return redirect(url_for('crear_productos'))
        
        conexion = obtener_conexion()
        if not conexion:
            flash("Error de conexión a la base de datos", "danger")
            return redirect(url_for('crear_productos'))
        
        try:
            cursor = conexion.cursor()
            cursor.execute(
                "INSERT INTO productos (nombre, precio, stock) VALUES (%s, %s, %s)",
                (nombre, precio, stock)
            )
            conexion.commit()
            flash("Producto creado exitosamente", "success")
            return redirect(url_for('productos'))  # Redirige a 'productos' no a 'listar_productos'
        except Exception as e:
            flash(f"Error al crear producto: {str(e)}", "danger")
            return redirect(url_for('crear_productos'))
        finally:
            if conexion.is_connected():
                cursor.close()
                conexion.close()
    
    return render_template('crear_productos.html')

# Ruta para manejar edición de productos (GET y POST)
@app.route('/editar_productos/<int:id>', methods=['GET', 'POST'])
#@login_required
def editar_producto(id):
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)
        
        # Verificar si el producto existe
        cursor.execute("SELECT * FROM productos WHERE id_producto = %s", (id,))
        producto = cursor.fetchone()
        
        if not producto:
            flash('El producto solicitado no existe', 'error')
            return redirect(url_for('productos'))
            
        if request.method == 'POST':
            # Procesar la edición
            nombre = request.form['nombre']
            precio = Decimal(request.form['precio'])
            stock = int(request.form['stock'])
            
            cursor.execute(
                "UPDATE productos SET nombre = %s, precio = %s, stock = %s WHERE id_producto = %s",
                (nombre, precio, stock, id)
            )
            conexion.commit()
            flash('Producto actualizado exitosamente', 'success')
            return redirect(url_for('productos'))
            
        # Mostrar formulario de edición (GET)
        return render_template('editar_productos.html', producto=producto)
        
    except Exception as e:
        flash(f'Error al procesar la solicitud: {str(e)}', 'danger')
        return redirect(url_for('productos'))
    finally:
        if 'conexion' in locals() and conexion.is_connected():
            conexion.close()

# Ruta para manejar eliminación de productos (GET y POST)
@app.route('/eliminar_productos/<int:id>', methods=['GET', 'POST'])
#@login_required
def eliminar_producto(id):
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)
        
        # Verificar si el producto existe
        cursor.execute("SELECT * FROM productos WHERE id_producto = %s", (id,))
        producto = cursor.fetchone()
        
        if not producto:
            flash('El producto solicitado no existe', 'error')
            return redirect(url_for('productos'))
            
        if request.method == 'POST':
            # Procesar la eliminación
            cursor.execute("DELETE FROM productos WHERE id_producto = %s", (id,))
            conexion.commit()
            flash('Producto eliminado exitosamente', 'success')
            return redirect(url_for('productos'))
            
        # Mostrar confirmación de eliminación (GET)
        return render_template('eliminar_productos.html', producto=producto)
        
    except Exception as e:
        flash(f'Error al procesar la solicitud: {str(e)}', 'danger')
        return redirect(url_for('productos'))
    finally:
        if 'conexion' in locals() and conexion.is_connected():
            conexion.close()

if __name__ == '__main__':
    app.run(debug=True)