from flask import Flask
import os
from routes.api import api_bp
from routes.views import views_bp

app = Flask(__name__)
app.secret_key = 's3cr3t_k3y'  

# Configuration for file uploads
UPLOAD_FOLDER = os.path.join('static/uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Register Blueprints
app.register_blueprint(views_bp)
app.register_blueprint(api_bp)

if __name__ == '__main__':
    app.run(debug=True)