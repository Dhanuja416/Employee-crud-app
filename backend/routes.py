from flask import Blueprint, request, jsonify
from models import db, Employee

# Create Blueprint for employee routes
employee_bp = Blueprint('employees', __name__)

# Health check endpoint
@employee_bp.route('/')
def home():
    return {"message": "Employee API is running!", "status": "healthy"}


# CREATE - Add new employee
@employee_bp.route('/api/employees', methods=['POST'])
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
@employee_bp.route('/api/employees', methods=['GET'])
def get_employees():
    try:
        employees = Employee.query.all()
        return jsonify([emp.to_dict() for emp in employees]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# READ - Get single employee
@employee_bp.route('/api/employees/<int:id>', methods=['GET'])
def get_employee(id):
    try:
        employee = Employee.query.get_or_404(id)
        return jsonify(employee.to_dict()), 200
    except Exception as e:
        return jsonify({'error': 'Employee not found'}), 404


# UPDATE - Update employee
@employee_bp.route('/api/employees/<int:id>', methods=['PUT'])
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
@employee_bp.route('/api/employees/<int:id>', methods=['DELETE'])
def delete_employee(id):
    try:
        employee = Employee.query.get_or_404(id)
        db.session.delete(employee)
        db.session.commit()
        return jsonify({'message': 'Employee deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
