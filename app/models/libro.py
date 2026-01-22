from app import db
class Socio(db.Model):
    __tablename__ = 'socios'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    libros = db.relationship('Libro', backref='socio', lazy=True)


class Libro(db.Model):
    __tablename__ = 'libros'
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    autor = db.Column(db.String(100), nullable=False)
    año = db.Column(db.Integer)
    categoria = db.Column(db.String(100))
    socio_id = db.Column(db.Integer, db.ForeignKey('socios.id'), nullable=True)


    def to_dict(self):
        return {
            "codigo": self.id,
            "titulo": self.titulo,
            "autor": self.autor,
            "año": self.año,
            "categoria": self.categoria,
            "codigo_socio": self.socio_id
        }