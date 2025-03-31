from flask_login import UserMixin
from Conexion.conexion import obtener_conexion
from werkzeug.security import check_password_hash, generate_password_hash

class Usuario(UserMixin):
    def __init__(self, id_usuario, nombre, email, password):
        self.id = id_usuario
        self.nombre = nombre
        self.email = email
        self.password = password

    def verificar_password(self, password):
        return check_password_hash(self.password, password)

    @classmethod
    def obtener_por_email(cls, email):
        conexion = obtener_conexion()
        if conexion:
            try:
                with conexion.cursor(dictionary=True) as cursor:
                    cursor.execute(
                        "SELECT id_usuario, nombre, email, password FROM usuarios WHERE email = %s",
                        (email,)
                    )
                    usuario = cursor.fetchone()
                    if usuario:
                        return cls(
                            id_usuario=usuario['id_usuario'],
                            nombre=usuario['nombre'],
                            email=usuario['email'],
                            password=usuario['password']
                        )
            except Exception as e:
                print(f"Error en obtener_por_email: {str(e)}")
            finally:
                if conexion.is_connected():
                    conexion.close()
        return None

    @classmethod
    def obtener_por_id(cls, id_usuario):
        conexion = obtener_conexion()
        if conexion:
            try:
                with conexion.cursor(dictionary=True) as cursor:
                    cursor.execute(
                        "SELECT id_usuario, nombre, email, password FROM usuarios WHERE id_usuario = %s",
                        (id_usuario,)
                    )
                    usuario = cursor.fetchone()
                    if usuario:
                        return cls(
                            id_usuario=usuario['id_usuario'],
                            nombre=usuario['nombre'],
                            email=usuario['email'],
                            password=usuario['password']
                        )
            except Exception as e:
                print(f"Error en obtener_por_id: {str(e)}")
            finally:
                if conexion.is_connected():
                    conexion.close()
        return None