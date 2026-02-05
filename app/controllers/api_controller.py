from flask import Blueprint, jsonify
from app.services.libros_service import listar_libros, listar_disponibles, buscar_libros
from app.models.user import User

api_bp = Blueprint("api", __name__, url_prefix="/api")

# Listar todos
@api_bp.route("/libros", methods=["GET"])
def listar():
    libros = listar_libros()
    return jsonify([libro.to_dict() for libro in libros])

# Listar disponibles
@api_bp.route("/libros/disponibles", methods=["GET"])
def disponibles():
    libros = listar_disponibles()
    return jsonify([libro.to_dict() for libro in libros])

# Buscar por título
@api_bp.route("/libros/buscar/<titulo>", methods=["GET"])
def buscar(titulo):
    libros = buscar_libros(titulo)
    return jsonify([libro.to_dict() for libro in libros])

# Listar socios con prestamo
@api_bp.route("/socios/prestamos", methods=["GET"])
def socios_con_prestamos():
    # Buscar socios con libros prestados
    socios = User.query.filter(User.libros.any()).all()
    resultado = []

    for socio in socios: 
        for libro in socio.libros:
            resultado.append({
                "socio_id": socio.id,
                "socio_nombre": socio.nombre,
                "socio_email": socio.email,
                "libro_id": libro.id,
                "libro_titulo": libro.titulo,
                "libro_autor": libro.autor
            })

    return jsonify(resultado)