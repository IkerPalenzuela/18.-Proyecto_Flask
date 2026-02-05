from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_required
from app.services import libros_service, user_service
from app.forms.libro_form import LibroForm
from app.forms.buscar_form import BuscarForm
from app.decorators.role_decorator import role_required

libros_bp = Blueprint("libros", __name__, url_prefix="/libros")

# Vista en lista para cualquier usuario sin necesidad de login
@libros_bp.route("/")
def listar():
    libros = libros_service.listar_libros()
    return render_template("paginas/libros/libros.html", libros=libros)

# Vista en grid, cualquiera puede acceder sin necesidad de login
@libros_bp.route("/grid")
def grid():
    libros = libros_service.listar_libros()
    return render_template("paginas/libros/librosGrid.html", libros=libros)

# Crear libro - Solo admins
@libros_bp.route("/crear", methods=["GET", "POST"])
@login_required
@role_required('admin')
def crear():
    form = LibroForm()
    
    if form.validate_on_submit():
        libros_service.crear_libro(
            form.titulo.data, 
            form.autor.data, 
            form.anio.data, 
            form.categoria.data
        )
        flash("Libro creado correctamente")
        return redirect(url_for("libros.listar"))
            
    return render_template("paginas/libros/libro_crear.html", form=form)

# Editar libro - Solo admins
@libros_bp.route("/<int:id>/editar", methods=["GET", "POST"])
@login_required
@role_required('admin')
def editar(id):
    libro = libros_service.obtener_libro(id)
    
    if not libro:
        flash("El libro no existe")
        return redirect(url_for("libros.listar"))
    
    form = LibroForm(obj=libro)
    
    if form.validate_on_submit():
        libros_service.editar_libro(
            id,
            titulo=form.titulo.data,
            autor=form.autor.data,
            anio=form.anio.data,
            categoria=form.categoria.data
        )
        flash("Libro editado correctamente")
        return redirect(url_for("libros.listar"))

    return render_template("paginas/libros/libro_editar.html", form=form, libro=libro)

# Prestar libro - Solo admins
@libros_bp.route("/<int:id>/prestar", methods=["GET", "POST"])
@login_required
@role_required('admin')
def prestar(id):
    libro = libros_service.obtener_libro(id)
    
    if not libro:
        flash("El libro no existe")
        return redirect(url_for("libros.listar"))
    
    socios = user_service.UserService.get_all_socios()
    
    if request.method == "POST":
        socio_id = request.form.get('socio_id')
        exito, mensaje = libros_service.prestar_libro(id, socio_id)
        
        if exito:
            flash(mensaje)
            return redirect(url_for("libros.listar"))
        else:
            flash(mensaje)

    return render_template("paginas/libros/libro_prestar.html", libro=libro, socios=socios)

# Devolver libro - Solo admins
@libros_bp.route("/<int:id>/devolver")
@login_required
@role_required('admin')
def devolver(id):
    exito, mensaje = libros_service.devolver_libro(id)
    flash(mensaje)
    return redirect(url_for("libros.listar"))

# Ver prestamos activos
@libros_bp.route("/prestamos")
def prestamos():
    # Obtenemos los socios con libros prestados
    socio_con_libros = user_service.UserService.get_all_socios()
    # Filtramos solo los socios que tienen libros prestados
    socios_con_prestamos = [socio for socio in socio_con_libros if socio.libros]

    return render_template("paginas/libros/prestamos.html", socios=socios_con_prestamos)

# Buscar libros por tiutulos in necesidad de login
@libros_bp.route("/buscar", methods=["GET", "POST"])
def buscar():
    form = BuscarForm()
    libros = []
    
    # Solo realizamos la búsqueda si el formulario es válido y se ha enviado
    if form.validate_on_submit():
        libros = libros_service.buscar_libros(form.busqueda.data)
    
    return render_template("paginas/libros/libro_buscar.html", form=form, libros=libros)