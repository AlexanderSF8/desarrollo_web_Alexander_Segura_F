import flask
from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.utils import secure_filename
from database.db import SessionLocal
from database.models import Comuna, Miembro, Actividad, Foto
from sqlalchemy import desc
from sqlalchemy.orm import joinedload
import os
import re
import json
from utils.validations import validate_registro_miembro, validate_datos_actividad

app = Flask(__name__)
app.secret_key = 's3cr3t_k3y'  
UPLOAD_FOLDER = os.path.join('static/uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    db_session = SessionLocal()
    last_members=db_session.query(Miembro)\
    .options(joinedload(Miembro.comuna).joinedload(Comuna.region))\
    .order_by(desc(Miembro.fecha_registro))\
    .limit(5)\
    .all()
    return render_template('index.html', members=last_members)

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

        # Validations
        if not validate_registro_miembro(name, email, phone, category, comuna_id):
            flash('Error en los datos de registro. Revisa el formato de los campos.', 'error')
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
    if 'miembro_id' not in session:
        flash('Acceso Denegado: debes registrarte primero.', 'error')
        return redirect(url_for('register'))

    miembro_id = session.get('miembro_id')

    if request.method == 'POST':
        datos_form = {
            'descripcion': request.form.get('activity'),
            'dias': request.form.get('dias_semana'),
            'horas': request.form.get('horas_dia'),
            'enlace': request.form.get('enlace'),
            'año_ingreso': request.form.get('año_ingreso') or None,  
            'telegram': request.form.get('telegram') or None,  
            'cargo': request.form.get('cargo') or None,  
            'area': request.form.get('area') or None,  
            'ramos': request.form.get('ramos') or None,  
            'investigacion': request.form.get('investigacion') or None  
        }
        fotos = request.files.getlist('archivos')
        miembro_categoria = session.get('user_category', '')

        if not validate_datos_actividad(miembro_categoria, datos_form, fotos):
            flash('Error en los datos o archivos ingresados.', 'error')
            return redirect(url_for('activities'))

        db = SessionLocal()
        try:
            nueva_actividad = Actividad(
                miembro_id=miembro_id,
                tipo=json.dumps(request.form.getlist('actividades')),
                descripcion=datos_form['descripcion'],
                dias_semana=int(datos_form['dias']),
                horas_dia=float(datos_form['horas']),
                enlace=datos_form['enlace'],
                año_ingreso=datos_form['año_ingreso'],
                telegram=datos_form['telegram'],
                cargo=datos_form['cargo'],
                area=datos_form['area'],
                ramos=datos_form['ramos'],
                investigacion=datos_form['investigacion']
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
    categoria_user = session.get('user_category', '')  
    return render_template('activities.html', categoria=categoria_user)

@app.route('/list')
def list_members():
    db = SessionLocal()
    try:
        members_db = db.query(Miembro).all() #get all members from the database
        members_list = []

        for member in members_db:
            activities_list = []
            # Iterate through the activities related to this member
            for activity in member.actividades:
                try:
                    type_list = json.loads(activity.tipo) # Decode the JSON string back into a Python list
                except (json.JSONDecodeError, TypeError):
                    type_list = []  # Fallback to an empty list if decoding fails

                # format photo data
                formatted_photos = [{'filename': foto.nombre_archivo} for foto in activity.fotos]
                activities_list.append({
                    'type_list': type_list,
                    'days_per_week': activity.dias_semana,
                    'hours_per_day': activity.horas_dia,
                    'description': activity.descripcion,
                    'link': activity.enlace,
                    'photos': formatted_photos
                })
                # Get the first activity to extract specific profile details (if available)
            primary_activity = member.actividades[0] if member.actividades else None

            members_list.append({
                'nombre': member.nombre,
                'email': member.email,
                'phone': member.telefono,
                'category': member.categoria,
                # Safe attribute retrieval using getattr to avoid crashes
                'entry_year': getattr(primary_activity, 'año_ingreso', 'N/A') if primary_activity else 'N/A',
                'telegram': getattr(primary_activity, 'telegram', 'N/A') if primary_activity else 'N/A',
                'department': getattr(primary_activity, 'area', 'N/A') if primary_activity else 'N/A',
                'role': getattr(primary_activity, 'cargo', 'N/A') if primary_activity else 'N/A',
                'courses': getattr(primary_activity, 'ramos', 'N/A') if primary_activity else 'N/A',
                'research_area': getattr(primary_activity, 'investigacion', 'N/A') if primary_activity else 'N/A',
                'activities': activities_list
            })
        return render_template('list.html', members=members_list)
    except Exception as e:
            print(f"Error al cargar lista de miembros: {e}")
            flash('Error al cargar la lista de miembros.', 'error')
            return render_template('list.html', members=[])
    finally:
        db.close()

@app.route('/statistics')
def statistics():
    return render_template('statistics.html')

if __name__ == '__main__':
    app.run(debug=True)