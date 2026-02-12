from app import db

class Libro(db.Model):
    # Creamos la tabla libros con sus columnas
    __tablename__ = 'libros'
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    autor = db.Column(db.String(100), nullable=False)
    anio = db.Column(db.Integer)
    categoria = db.Column(db.String(100))
    socio_id = db.Column(db.Integer, db.ForeignKey('socios.id'), nullable=True)

    # Metodo para convertir el libro a un diccionario
    def to_dict(self):
        return {
            "id": self.id,
            "titulo": self.titulo,
            "autor": self.autor,
            "anio": self.anio,
            "categoria": self.categoria,
            "estado": "Prestado" if self.socio_id else "Disponible"
        }
    
    # Metodo para saber si el libro esta disponible
    def esta_disponible(self):
        return self.socio_id is None