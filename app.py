from flask import Flask

app = Flask(__name__)


@app.route('/')
def bienvenidaPredeterminada():
    return '¡Hola, bienvenido a mi proyecto Flask!'

#Nueva ruta con mensaje de bienvenida personalizado
@app.route('/usuario/<nombre>')
def usuario(nombre):
    return f'¡Bienvenido, {nombre}!'

if __name__ == '__main__':
    app.run()
