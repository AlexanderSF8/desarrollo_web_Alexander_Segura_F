from flask import Blueprint, jsonify , request
from sqlalchemy import func
from database.db import SessionLocal
from database.models import Comentario, Miembro, Actividad, Comuna

# Creamos el Blueprint. 
api_bp = Blueprint('api', __name__, url_prefix='/api')

# Line graph
@api_bp.route('/stats/members-per-day')
def stats_members_per_day():
    db_session = SessionLocal()
    try:
        resultados = db_session.query(
            func.date(Miembro.fecha_registro).label('fecha'),
            func.count(Miembro.id).label('cantidad')
        ).group_by(func.date(Miembro.fecha_registro)).order_by(func.date(Miembro.fecha_registro)).all()

        datos = [{"fecha": str(r.fecha), "cantidad": r.cantidad} for r in resultados]
        return jsonify(datos)
    finally:
        db_session.close()

# Pie graph
@api_bp.route('/stats/activities-by-type')
def stats_activities_by_type():
    db_session = SessionLocal()
    try:
        resultados = db_session.query(
            Actividad.tipo,
            func.count(Actividad.id).label('cantidad')
        ).group_by(Actividad.tipo).all()

        datos = [{"tipo": r.tipo, "cantidad": r.cantidad} for r in resultados]
        return jsonify(datos)
    finally:
        db_session.close()

# Bar graph
@api_bp.route('/stats/activities-by-commune')
def stats_activities_by_commune():
    db_session = SessionLocal()
    try:
        resultados = db_session.query(
            Comuna.nombre,
            func.count(Actividad.id).label('cantidad')
        ).join(Miembro, Actividad.miembro_id == Miembro.id)\
         .join(Comuna, Miembro.comuna_id == Comuna.id)\
         .group_by(Comuna.nombre).all()

        datos = [{"comuna": r.nombre, "cantidad": r.cantidad} for r in resultados]
        return jsonify(datos)
    finally:
        db_session.close()


#-----------------------------
# Routes for Comments Section
#-----------------------------

# GET comments for a specific activity
@api_bp.route('/comments/<int:actividad_id>', methods=['GET'])
def get_comments(actividad_id):
    db_session = SessionLocal()
    try:
        # Search for comments linked to the given activity ID, ordered by most recent first
        comentarios = db_session.query(Comentario).filter(
            Comentario.actividad_id == actividad_id
        ).order_by(Comentario.fecha.desc()).all()

        # Transform the comment objects into a list of dictionaries to send as JSON
        datos = []
        for c in comentarios:
            datos.append({
                "id": c.id,
                "nombre": c.nombre, 
                "texto": c.texto,
                "fecha": c.fecha.strftime("%d-%m-%Y %H:%M") 
            })
            
        return jsonify(datos), 200
    except Exception as e:
        print(f"Error al cargar comentarios: {e}")
        return jsonify({'error': 'Error al cargar los comentarios'}), 500
    finally:
        db_session.close()


# POST a new comment for a specific activity
@api_bp.route('/comments', methods=['POST'])
def add_comment():
    db_session = SessionLocal()
    try:
        # Get the JSON data sent by the client
        data = request.get_json()
        
        actividad_id = data.get('actividad_id')
        nombre = data.get('nombre', '').strip()
        texto = data.get('texto', '').strip()

        # Server Validation
        if not actividad_id or not nombre or not texto:
            return jsonify({'error': 'Faltan datos obligatorios.'}), 400
            
        if len(nombre) < 3 or len(nombre) > 80:
            return jsonify({'error': 'El nombre debe tener entre 3 y 80 caracteres.'}), 400
            
        if len(texto) < 5 or len(texto) > 300:
            return jsonify({'error': 'El comentario debe tener entre 5 y 300 caracteres.'}), 400

        # transaction to save the new comment in the database
        nuevo_comentario = Comentario(
            actividad_id=actividad_id,
            nombre=nombre,
            texto=texto
        )
        
        db_session.add(nuevo_comentario)
        db_session.commit() 
        
        return jsonify({'message': 'Comentario guardado exitosamente.'}), 201
        
    except Exception as e:
        db_session.rollback() 
        print(f"Error al guardar comentario: {e}")
        return jsonify({'error': 'Error interno del servidor al intentar guardar.'}), 500
    finally:
        db_session.close()