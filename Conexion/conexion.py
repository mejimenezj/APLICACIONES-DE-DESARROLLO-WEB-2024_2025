from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def conectar(app):
    # Configurar la base de datos MySQL
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:admin@127.0.0.1:3306/desarrollo_web'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)  # Inicializa la conexión con la aplicación Flask

    return db
