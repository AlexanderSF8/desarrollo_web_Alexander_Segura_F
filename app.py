from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.utils import secure_filename
import os
import re

app = Flask(__name__)
app.secret_key = 's3cr3t_k3y'  
UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Funciones de validación
def validate_email(email):
    return re.match(r'^[^@\s]+@[^@\s]+\.[^@\s]+$', email)

def validate_form_data(data):
    for field, value in data.items():
        if value is None or not str(value).strip():
            return False, f"El campo '{field}' no puede estar vacío o es inválido."
    return True, None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        category = request.form.get('select-department')
        terms = request.form.get('terminos')

        # Validaciones
        valid, error = validate_form_data({
            'Nombre': name,
            'Correo Electrónico': email,
            'Teléfono': phone,
            'Categoría': category,
            'Términos': terms
        })
        if not valid:
            flash(error, 'error')
            return redirect(url_for('register'))

        if not validate_email(email):
            flash('El correo electrónico no es válido.', 'error')
            return redirect(url_for('register'))

        # Guardar la categoría en la sesión
        session['user_category'] = category
        flash('Registro exitoso.', 'success')
        return redirect(url_for('activities'))

    return render_template('register.html')

@app.route('/activities', methods=['GET', 'POST'])
def activities():
    if request.method == 'POST':
        activity_type = request.form.getlist('actividades')
        description = request.form.get('activity')
        files = request.files.getlist('archivos')
        link = request.form.get('enlace')

        # Validaciones
        valid, error = validate_form_data({
            'Descripción de la Actividad': description,
            'Enlace': link
        })
        if not valid:
            flash(error, 'error')
            return redirect(url_for('activities'))

        for file in files:
            if file.filename:
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        flash('Actividad registrada exitosamente.', 'success')
        return redirect(url_for('list_members'))

    return render_template('activities.html')

@app.route('/list')
def list_members():
    return render_template('list.html')

@app.route('/statistics')
def statistics():
    return render_template('statistics.html')

if __name__ == '__main__':
    app.run(debug=True)