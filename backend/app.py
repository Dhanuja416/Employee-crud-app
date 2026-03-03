from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Enable CORS (Cross-Origin Resource Sharing)
# This allows our React frontend (port 3000) to talk to Flask backend (port 5000)
CORS(app)

# Database configuration
# SQLAlchemy will use our PostgreSQL database
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db = SQLAlchemy(app)

# Define Employee Model
# This class represents the 'employees' table in our database
class Employee(db.Model):
    __tablename__ = 'employees'
    
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    position = db.Column(db.String(100), nullable=False)
    salary = db.Column(db.Numeric(10, 2), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    
    def to_dict(self):
        """Convert employee object to dictionary for JSON response"""
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'position': self.position,
            'salary': float(self.salary),
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

# Create tables
with app.app_context():
    db.create_all()

# Health check endpoint
@app.route('/')
def home():
    return {"message": "Employee API is running!", "status": "healthy"}


    # CREATE - Add new employee
@app.route('/api/employees', methods=['POST'])
def create_employee():
    try:
        data = request.get_json()
        
        # Validation
        required_fields = ['first_name', 'last_name', 'email', 'position', 'salary']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'{field} is required'}), 400
        
        # Check if email already exists
        existing = Employee.query.filter_by(email=data['email']).first()
        if existing:
            return jsonify({'error': 'Email already exists'}), 409
        
        # Create new employee
        new_employee = Employee(
            first_name=data['first_name'],
            last_name=data['last_name'],
            email=data['email'],
            position=data['position'],
            salary=data['salary']
        )
        
        db.session.add(new_employee)
        db.session.commit()
        
        return jsonify(new_employee.to_dict()), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# READ - Get all employees
@app.route('/api/employees', methods=['GET'])
def get_employees():
    try:
        employees = Employee.query.all()
        return jsonify([emp.to_dict() for emp in employees]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# READ - Get single employee
@app.route('/api/employees/<int:id>', methods=['GET'])
def get_employee(id):
    try:
        employee = Employee.query.get_or_404(id)
        return jsonify(employee.to_dict()), 200
    except Exception as e:
        return jsonify({'error': 'Employee not found'}), 404

# UPDATE - Update employee
@app.route('/api/employees/<int:id>', methods=['PUT'])
def update_employee(id):
    try:
        employee = Employee.query.get_or_404(id)
        data = request.get_json()
        
        # Update fields if provided
        if 'first_name' in data:
            employee.first_name = data['first_name']
        if 'last_name' in data:
            employee.last_name = data['last_name']
        if 'email' in data:
            # Check if new email already exists for different employee
            existing = Employee.query.filter_by(email=data['email']).first()
            if existing and existing.id != id:
                return jsonify({'error': 'Email already exists'}), 409
            employee.email = data['email']
        if 'position' in data:
            employee.position = data['position']
        if 'salary' in data:
            employee.salary = data['salary']
        
        db.session.commit()
        return jsonify(employee.to_dict()), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# DELETE - Delete employee
@app.route('/api/employees/<int:id>', methods=['DELETE'])
def delete_employee(id):
    try:
        employee = Employee.query.get_or_404(id)
        db.session.delete(employee)
        db.session.commit()
        return jsonify({'message': 'Employee deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)