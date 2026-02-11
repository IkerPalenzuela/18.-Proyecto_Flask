from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required
from app.forms.socio_form import SocioForm 
from app.services import socios_service
from app.decorators.role_decorator import role_required

socios_bp = Blueprint("socios", __name__, url_prefix="/socios")

@socios_bp.route("/")
@login_required
@role_required('admin')
def listar():
    socios = socios_service.listar_todos()
    return render_template("paginas/socios/socios.html", socios=socios)

@socios_bp.route("/crear", methods=["GET", "POST"])
@login_required
@role_required('admin')
def crear():
    form = SocioForm()
    
    if form.validate_on_submit():
        exito, mensaje = socios_service.crear_socio(
            nombre=form.nombre.data,
            email=form.email.data
        )
        flash(mensaje, "success" if exito else "error")
        
        if exito:
            return redirect(url_for("socios.listar"))
    
    return render_template("paginas/socios/socios_crear.html", form=form)

@socios_bp.route("/<int:id>/editar", methods=["GET", "POST"])
@login_required
@role_required('admin')
def editar(id):
    socio = socios_service.obtener_por_id(id)
    
    if not socio:
        flash("El socio no existe", "error")
        return redirect(url_for("socios.listar"))
    
    form = SocioForm(obj=socio)
    
    if form.validate_on_submit():
        exito, mensaje = socios_service.editar_socio(
            id=id,
            nombre=form.nombre.data,
            email=form.email.data
        )
        flash(mensaje, "success" if exito else "error")
        
        if exito:
            return redirect(url_for("socios.listar"))

    return render_template("paginas/socios/socios_editar.html", form=form, socio=socio)

@socios_bp.route("/<int:id>/borrar", methods=["POST"])
@login_required
@role_required('admin')
def borrar(id):
    exito, mensaje = socios_service.borrar_socio(id)
    flash(mensaje, "success" if exito else "error")
    return redirect(url_for("socios.listar"))