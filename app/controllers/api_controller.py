from flask import Blueprint, jsonify
from app.services import libros_service, socios_service

api_bp = Blueprint("api", __name__, url_prefix="/api")

# Listar todos los libros
@api_bp.route("/libros", methods=["GET"])
def listar():
    libros = libros_service.listar_libros()
    return jsonify([libro.to_dict() for libro in libros])

# Listar libros disponibles
@api_bp.route("/libros/disponibles", methods=["GET"])
def disponibles():
    libros = libros_service.listar_disponibles()
    return jsonify([libro.to_dict() for libro in libros])

# Buscar por título
@api_bp.route("/libros/buscar/<titulo>", methods=["GET"])
def buscar(titulo):
    libros = libros_service.buscar_libros(titulo)
    return jsonify([libro.to_dict() for libro in libros])

# Listar socios con préstamo
@api_bp.route("/socios/prestamos", methods=["GET"])
def socios_con_prestamos():
    resultado = socios_service.obtener_listado_prestamos_api()
    return jsonify(resultado)