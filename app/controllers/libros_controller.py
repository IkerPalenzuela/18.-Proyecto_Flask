from flask import Blueprint, request, render_template, redirect, url_for
from app.models import Libro, Socio, db
from app.forms.libro_form import LibroForm

libros_bp = Blueprint("libros", __name__, url_prefix="/libros")

@libros_bp.route("/")
def listar():
    libros = Libro.query.all()
    return render_template("paginas/libros/libros.html", libros=libros)

@libros_bp.route("/crear", methods=["GET", "POST"])
def crear():
    form = LibroForm()
    if request.method == "POST":
        if form.validate_on_submit():
            nuevo_libro = Libro(
                titulo=form.titulo.data,
                autor=form.autor.data,
                año=form.anio.data,
                categoria=form.categoria.data
            )
            db.session.add(nuevo_libro)
            db.session.commit()
            return redirect(url_for("libros.listar"))
    return render_template("paginas/libros/libro_crear.html", form=form)

@libros_bp.route("/<int:id>/editar", methods=["GET","POST"])
def editar(id):
    libro = Libro.query.get_or_404(id)
    form = LibroForm(obj=libro)
    
    if request.method == "POST":
        if form.validate_on_submit():
            libro.titulo = form.titulo.data
            libro.autor = form.autor.data
            libro.año = form.anio.data
            libro.categoria = form.categoria.data
            
            db.session.commit()
            return redirect(url_for("libros.listar"))

    return render_template("paginas/libros/libro_editar.html", form=form, libro=libro)

@libros_bp.route("/<int:id>/prestar", methods=["GET", "POST"])
def prestar(id):
    libro = Libro.query.get_or_404(id)
    socios = Socio.query.all()
    
    if request.method == "POST":
        socio_id = request.form.get('socio_id')
        libro.socio_id = socio_id
        db.session.commit()
        return redirect(url_for("libros.listar"))

    return render_template("paginas/libros/libro_prestar.html", libro=libro, socios=socios)

@libros_bp.route("/<int:id>/devolver")
def devolver(id):
    libro = Libro.query.get_or_404(id)
    libro.socio_id = None
    db.session.commit()
    return redirect(url_for("libros.listar"))