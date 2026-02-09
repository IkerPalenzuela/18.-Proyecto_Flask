from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_required
from app.services import libro_service, socio_service # Importamos socio_service
from app.forms.libro_form import LibroForm
from app.forms.buscar_form import BuscarForm
from app.decorators.role_decorator import role_required

libros_bp = Blueprint("libros", __name__, url_prefix="/libros")

# Listado público
@libros_bp.route("/")
def listar():
    libros = libro_service.listar_libros()
    return render_template("paginas/libros/libros.html", libros=libros)

# Crear libro (Admin)
@libros_bp.route("/crear", methods=["GET", "POST"])
@login_required
@role_required('admin')
def crear():
    form = LibroForm()
    
    if form.validate_on_submit():
        libro_service.crear_libro(
            form.titulo.data, 
            form.autor.data, 
            form.anio.data, 
            form.categoria.data
        )
        flash("Libro creado correctamente", "success")
        return redirect(url_for("libros.listar"))
            
    return render_template("paginas/libros/libro_crear.html", form=form)

# Editar libro (Admin)
@libros_bp.route("/<int:id>/editar", methods=["GET", "POST"])
@login_required
@role_required('admin')
def editar(id):
    libro = libro_service.obtener_libro(id)
    
    if not libro:
        flash("El libro no existe", "error")
        return redirect(url_for("libros.listar"))
    
    form = LibroForm(obj=libro)
    
    if form.validate_on_submit():
        libro_service.editar_libro(
            id,
            titulo=form.titulo.data,
            autor=form.autor.data,
            anio=form.anio.data,
            categoria=form.categoria.data
        )
        flash("Libro editado correctamente", "success")
        return redirect(url_for("libros.listar"))

    return render_template("paginas/libros/libro_editar.html", form=form, libro=libro)

# Borrar libro (Admin)
@libros_bp.route("/<int:id>/borrar", methods=["POST"])
@login_required
@role_required('admin')
def borrar(id):
    exito, mensaje = libro_service.borrar_libro(id)
    flash(mensaje, "success" if exito else "error")
    return redirect(url_for("libros.listar"))

# Prestar libro (Admin)
@libros_bp.route("/<int:id>/prestar", methods=["GET", "POST"])
@login_required
@role_required('admin')
def prestar(id):
    libro = libro_service.obtener_libro(id)
    if not libro:
        flash("El libro no existe")
        return redirect(url_for("libros.listar"))
    
    socios = socio_service.listar_todos()
    
    if request.method == "POST":
        socio_id = request.form.get('socio_id')
        exito, mensaje = libro_service.prestar_libro(id, socio_id)
        
        flash(mensaje, "success" if exito else "error")
        if exito:
            return redirect(url_for("libros.listar"))

    return render_template("paginas/libros/libro_prestar.html", libro=libro, socios=socios)

# Devolver libro (Admin)
@libros_bp.route("/<int:id>/devolver")
@login_required
@role_required('admin')
def devolver(id):
    exito, mensaje = libro_service.devolver_libro(id)
    flash(mensaje, "success" if exito else "error")
    return redirect(url_for("libros.listar"))

# Buscar libros (Público)
@libros_bp.route("/buscar", methods=["GET", "POST"])
def buscar():
    form = BuscarForm()
    libros = []
    
    if form.validate_on_submit():
        libros = libro_service.buscar_libros(form.busqueda.data)
    
    return render_template("paginas/libros/libro_buscar.html", form=form, libros=libros)