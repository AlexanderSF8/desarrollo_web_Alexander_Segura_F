from flask import Blueprint, jsonify
from sqlalchemy import func
from database.db import SessionLocal
from database.models import Miembro, Actividad, Comuna

# Creamos el Blueprint. 
api_bp = Blueprint('api', __name__, url_prefix='/api')
