from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required
from app.forms.user_form import UserForm
from app.services.user_service import UserService
from app.decorators.role_decorator import role_required

user_bp = Blueprint("user", __name__, url_prefix="/socios")

@user_bp.route("/")
def listar():
    socios = UserService.get_all_socios()
    return render_template("paginas/socios/socios.html", socios=socios)

@user_bp.route("/crear", methods=["GET", "POST"])
@login_required
@role_required('admin')
def crear():
    form = UserForm()
    
    if form.validate_on_submit():
        exito, mensaje = UserService.crear_socio(
            nombre=form.nombre.data,
            email=form.email.data,
            username=form.username.data,
            password=form.password.data
        )
        flash(mensaje, "success" if exito else "error")
        
        if exito:
            return redirect(url_for("user.listar"))
    
    return render_template("paginas/socios/socio_crear.html", form=form)

@user_bp.route("/<int:id>/editar", methods=["GET", "POST"])
@login_required
@role_required('admin')
def editar(id):
    socio = UserService.get_socio_by_id(id)
    
    if not socio:
        flash("El socio no existe", "error")
        return redirect(url_for("user.listar"))
    
    form = UserForm(obj=socio)
    
    if form.validate_on_submit():
        exito, mensaje = UserService.editar_socio(
            id=id,
            nombre=form.nombre.data,
            email=form.email.data
        )
        flash(mensaje, "success" if exito else "error")
        
        if exito:
            return redirect(url_for("user.listar"))

    return render_template("paginas/socios/socio_editar.html", form=form, socio=socio)

@user_bp.route("/<int:id>/borrar", methods=["POST"])
@login_required
@role_required('admin')
def borrar(id):
    exito, mensaje = UserService.borrar_socio(id)
    flash(mensaje, "success" if exito else "error")
    return redirect(url_for("user.listar"))

@user_bp.route("/prestamos")
def prestamos():
    socios = UserService.get_socios_con_prestamo()
    return render_template("paginas/socios/socios_prestamos.html", socios=socios)

@user_bp.route("/disponibles")
def disponibles():
    socios = UserService.get_socios_disponibles()
    return render_template("paginas/socios/socios_disponibles.html", socios=socios)