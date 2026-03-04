from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
import os

# Import database and models
from models import db

# Import routes
from routes import employee_bp

# Load environment variables
load_dotenv()

def create_app():
    """Application factory pattern"""
    # Initialize Flask app
    app = Flask(__name__)
    
    # Enable CORS (Cross-Origin Resource Sharing)
    # This allows our React frontend to communicate with Flask backend
    CORS(app)
    
    # Database configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize database with app
    db.init_app(app)
    
    # Register blueprints
    app.register_blueprint(employee_bp)
    
    # Create tables
    with app.app_context():
        db.create_all()
    
    return app

# Create app instance
app = create_app()

if __name__ == '__main__':
    app.run(debug=True, port=5000)