from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager 

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    CORS(app)

    # Configuración de la base de datos y Flask-Login
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///library.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False 
    app.config["SECRET_KEY"] = "dev-secret-key" 

    # Inicialización de extensiones
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login' 
    login_manager.login_message = "Debes iniciar sesión."

    # Registro de los Blueprints
    from app.controllers.navigation_controller import navigation_bp
    app.register_blueprint(navigation_bp)
    
    from app.controllers.libros_controller import libros_bp
    app.register_blueprint(libros_bp)

    from app.controllers.socios_controller import socios_bp
    app.register_blueprint(socios_bp)
    
    from app.controllers.api_controller import api_bp
    app.register_blueprint(api_bp)
    
    from app.controllers.auth_controller import auth_bp
    app.register_blueprint(auth_bp)

    # Crear las tablas en la base de datos
    with app.app_context():
        from app.models.libro import Libro
        from app.models.user import Usuario 
        from app.models.socio import Socio
        
        db.create_all()
        
        from app.services.user_service import UserService
        UserService.ensure_admin()

    return app

# Función para cargar el usuario actual a través de Flask-Login
@login_manager.user_loader
def load_user(user_id):
    from app.models.user import Usuario
    return Usuario.query.get(int(user_id))