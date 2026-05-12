import flask
from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.utils import secure_filename
from database.db import SessionLocal
from database.models import Miembro, Actividad, Foto
import os
import re
import json

app = Flask(__name__)
app.secret_key = 's3cr3t_k3y'  
UPLOAD_FOLDER = os.path.join('static/uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs('UPLOAD_FOLDER', exist_ok=True)

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
        region_id = request.form.get('region')
        comuna_id = request.form.get('comuna')

        # Validaciones
        valid, error = validate_form_data({
            'Nombre': name,
            'Correo Electrónico': email,
            'Teléfono': phone,
            'Categoría': category,
            'Region': region_id,
            'Comuna': comuna_id,
            'Términos': terms
        })
        if not valid:
            flash(error, 'error')
            return redirect(url_for('register'))

        if not validate_email(email):
            flash('El correo electrónico no es válido.', 'error')
            return redirect(url_for('register'))
        
        db = SessionLocal()
        # create a new member instance and add it to the database
        try: 
            nuevo_miembro = Miembro(
                nombre=name,
                email=email,
                telefono=phone,
                categoria=category,
                comuna_id=int(comuna_id)
            )
            db.add(nuevo_miembro)
            db.commit()

            # Save 
            session['user_category'] = category
            session['miembro_id'] = nuevo_miembro.id

            flash('Registro exitoso. Ahora completa este apartado', 'success')
            return redirect(url_for('activities'))
        except Exception as e:
            # error asociate with email uniqueness constraint
            db.rollback()
            flash('Error al registrar el miembro, puede que el correo ya esté registrado.', 'error')
            print(f"Error al registrar miembro: {e}")
            return redirect(url_for('register'))
        finally:
            db.close()

    return render_template('register.html')

@app.route('/activities', methods=['GET', 'POST'])
def activities():
    # First, verify that the user complete the registration form and has a valid session
    if 'miembro_id' not in session:
        flash('Acceso Denegado: debes registrarte primero.', 'error')
        return redirect(url_for('register'))
    miembro_id = session.get('miembro_id')


    if request.method == 'POST':
        activity_type = request.form.getlist('actividades')
        description = request.form.get('activity')
        days_week = request.form.get('dias_semana')
        hours_days = request.form.get('horas_dia')
        fotos = request.files.getlist('archivos')
        link = request.form.get('enlace')
        
        types_json = json.dumps(activity_type)  #convert list to JSON string for storage
        db = SessionLocal() 
        try:
            nueva_actividad = Actividad(
                miembro_id=miembro_id,
                tipo=types_json,
                descripcion=description,
                dias_semana=int(days_week),
                horas_dia=float(hours_days),
                enlace=link
            )
            db.add(nueva_actividad)
            db.commit()
            fotos=request.files.getlist('archivos')
            for foto in fotos:
                if foto and foto.filename:
                    filename = secure_filename(foto.filename)
                    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    foto.save(file_path)

                    nueva_foto = Foto(
                        ruta_archivo=file_path,
                        nombre_archivo=filename,
                        actividad_id=nueva_actividad.id
                    )
                    db.add(nueva_foto)
            db.commit()
            flash('Actividad registrada exitosamente.', 'success')
            session.pop('miembro_id', None)  # Clear the session after successful registration
            return redirect(url_for('index'))
        
        except Exception as e:
            db.rollback()
            flash('Error al registrar la actividad. Por favor, inténtalo de nuevo.', 'error')
            print(f"Error al registrar actividad: {e}")
            return redirect(url_for('activities'))
        finally:
            db.close()
    return render_template('activities.html')

@app.route('/list')
def list_members():
    return render_template('list.html')

@app.route('/statistics')
def statistics():
    return render_template('statistics.html')

if __name__ == '__main__':
    app.run(debug=True)