from flask import Blueprint, jsonify
from sqlalchemy import func
from database.db import SessionLocal
from database.models import Miembro, Actividad, Comuna

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