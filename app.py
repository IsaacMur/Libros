from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField, IntegerField, SelectField
from wtforms.validators import DataRequired, Length, ValidationError
from dao.libro_dao import LibroDAO
from cqrs.libro_cqrs import LibroCQRS 

app = Flask(__name__)
app.secret_key = 'tu_secreto' 
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'admin'
app.config['MYSQL_DB'] = 'biblioteca'

mysql = MySQL(app)

libro_dao = LibroDAO(mysql)
libro_cqrs = LibroCQRS(libro_dao)

class LoginForm(FlaskForm):
    username = StringField('Usuario', validators=[DataRequired(), Length(min=3, max=25)])
    password = PasswordField('Contraseña', validators=[DataRequired(), Length(min=3, max=35)])
    submit = SubmitField('Entrar')

class LibroForm(FlaskForm):
    nombre = StringField('Título', validators=[DataRequired()])
    autor = StringField('Autor', validators=[DataRequired()])
    genero = StringField('Género', validators=[DataRequired()])
    estatus = SelectField('Estatus', choices=[('', 'Selecciona un estatus'), ('0', 'No disponible'), ('1', 'Disponible')],
                          validators=[DataRequired(message='Debes seleccionar un estatus.')])
    archivo = FileField('Archivo PDF')

def login_required(f):
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            flash('Debes iniciar sesión para acceder a esta página.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    return redirect(url_for('login')) 

# L O G I N 
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM usuarios WHERE username = %s AND password = %s", (username, password))
        user = cur.fetchone()
        cur.close()
        
        if user:
            session['user'] = username
            return redirect(url_for('home')) 
        else:
            flash('Usuario o contraseña incorrectos', 'danger')
    
    return render_template('login.html', form=form)

# I N S E R T A R 
# I N S E R T A R 
@app.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    form = LibroForm()
    
    if form.validate_on_submit():
        nombre = form.nombre.data
        autor = form.autor.data
        genero = form.genero.data
        estatus = form.estatus.data
        archivo = request.files['archivo'].read()

        try:
            libro_cqrs.insertar_libro(nombre, autor, genero, estatus, archivo)
            flash('Libro creado exitosamente', 'success')  # Mensaje de éxito
            return redirect(url_for('home'))
        except ValidationError as e:
            flash(str(e), 'danger')  # Mensaje de error

    libros = libro_cqrs.obtener_todos_los_libros()
    
    return render_template('inicio.html', username=session['user'], form=form, libros=libros)


# E L I M I N A R 
@app.route('/eliminar_libro/<int:id_libro>')
@login_required
def eliminar_libro(id_libro):
    libro_cqrs.eliminar_libro(id_libro)
    flash('Libro eliminado exitosamente', 'info')  # Mensaje informativo
    return redirect(url_for('home'))


# E D I T A R 
@app.route('/editar_libro/<int:id_libro>', methods=['GET', 'POST'])
@login_required
def editar_libro(id_libro):
    libro = libro_cqrs.obtener_libro_por_id(id_libro)
    
    if not libro:
        flash('Libro no encontrado', 'danger')
        return redirect(url_for('home'))
    
    form = LibroForm()

    if form.validate_on_submit():
        nombre = form.nombre.data
        autor = form.autor.data
        genero = form.genero.data
        estatus = form.estatus.data

        if form.archivo.data:
            archivo = request.files['archivo'].read()
        else:
            archivo = libro[5]  

        try:
            libro_cqrs.actualizar_libro(id_libro, nombre, autor, genero, estatus, archivo)
            flash('Libro actualizado exitosamente', 'success')
            return redirect(url_for('home'))
        except ValidationError as e:
            flash(str(e), 'danger') 

    form.nombre.data = libro[1]
    form.autor.data = libro[2]
    form.genero.data = libro[3]
    form.estatus.data = libro[4]

    return render_template('editar_libro.html', form=form, libro=libro)


# V E R  P D F 
@app.route('/ver_pdf/<int:id_libro>')
@login_required
def ver_pdf(id_libro):
    libro = libro_dao.obtener_libro_por_id(id_libro)
    
    if libro:
        return app.response_class(libro[5], content_type='application/pdf')
    else:
        flash('Libro no encontrado', 'danger')
        return redirect(url_for('home'))


# C E R R A R   S E S I O N 
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True, port=8080)
