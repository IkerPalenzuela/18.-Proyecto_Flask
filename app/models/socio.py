from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db

class Socio(db.Model):
    __tablename__ = 'socios'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False) 
    libros = db.relationship('Libro', backref='socio', lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "email": self.email,
            "libros_prestados": [libro.to_dict() for libro in self.libros]
        }