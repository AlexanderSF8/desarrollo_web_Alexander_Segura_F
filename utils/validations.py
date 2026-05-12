import re
import filetype

# ==========================================
# ATOMIC VALIDATORS 
# ==========================================

def validate_text(value, min_length=0, max_length=None):
    if not value: return False
    if len(value) < min_length: return False
    if max_length and len(value) > max_length: return False
    return True

def validate_email(value):
    if not value: return False
    return bool(re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", value))

def validate_number(value, min_val, max_val):
    try:
        val = float(value)
        return min_val <= val <= max_val
    except (ValueError, TypeError):
        return False

def validate_telegram(value):
    return bool(value and value.startswith('@') and len(value) >= 4)

def validate_url(value):
    if not value: return True # Es opcional en tu BD
    return bool(re.match(r"^https?://", value))

def validate_file(file):
    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "mp4", "avi"}
    ALLOWED_MIMETYPES = {"image/jpeg", "image/png", "image/gif", "video/mp4", "video/x-msvideo"}

    if file is None or file.filename == "":
        return False
    
    ftype_guess = filetype.guess(file)
    if ftype_guess is None: return False
    return (ftype_guess.extension in ALLOWED_EXTENSIONS) and (ftype_guess.mime in ALLOWED_MIMETYPES)

# ==========================================
# COMPLEX VALIDATORS (USE ATOMIC VALIDATORS INSIDE)
# ==========================================

def validate_registro_miembro(nombre, email, telefono, categoria, comuna_id):
    """Valida todos los campos del primer formulario (/register)"""
    # Validate each field using atomic validators
    v_nombre = validate_text(nombre, min_length=3)
    v_email = validate_email(email)
    v_telefono = validate_text(telefono, min_length=8) # Asumiendo un mínimo para teléfonos
    
    categorias_validas = ['estudiante', 'funcionario', 'academico']
    v_categoria = categoria in categorias_validas
    
    v_comuna = validate_number(comuna_id, 1, 346) 

    return all([v_nombre, v_email, v_telefono, v_categoria, v_comuna])

def validate_datos_actividad(categoria, datos_form, archivos):
    """Valida la actividad dependiendo si es estudiante, funcionario o académico"""
    
    # validate common fields for all categories
    v_desc = validate_text(datos_form.get('descripcion'), min_length=10)
    v_dias = validate_number(datos_form.get('dias'), 1, 7)
    v_horas = validate_number(datos_form.get('horas'), 0.5, 24)
    v_enlace = validate_url(datos_form.get('enlace'))
    
    v_archivos = any(validate_file(f) for f in archivos)

    validate_all = all([v_desc, v_dias, v_horas, v_enlace, v_archivos])
    if not validate_all: 
        return False

    # 2. Validaciones Específicas por Categoría
    if categoria == 'estudiante':
        v_año = validate_number(datos_form.get('año_ingreso'), 2000, 2026)
        v_tele = validate_telegram(datos_form.get('telegram'))
        return all([v_año, v_tele])
        
    elif categoria == 'funcionario':
        v_cargo = validate_text(datos_form.get('cargo'), min_length=3)
        v_area = validate_text(datos_form.get('area'), min_length=3)
        return all([v_cargo, v_area])
        
    elif categoria == 'academico':
        v_ramos = validate_text(datos_form.get('ramos'), min_length=3)
        v_inv = validate_text(datos_form.get('investigacion'), min_length=3)
        return all([v_ramos, v_inv])

    return False