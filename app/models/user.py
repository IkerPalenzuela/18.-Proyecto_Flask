from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class Usuario(db.Model, UserMixin):
    # Creamos la tabla usuarios con sus columnas
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    rol = db.Column(db.String(20), default='admin')

    # Metodo para hashear la contraseña
    def set_password(self, password):
        self.password = generate_password_hash(password)

    # Metodo para verificar la contraseña
    def check_password(self, password):
        return check_password_hash(self.password, password)