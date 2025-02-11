# app.py
from flask import Flask, request, jsonify
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from config import Config
from database import Database
from models import UserModel, PropertyModel
import mysql.connector
from datetime import datetime

app = Flask(__name__)
app.config.from_object(Config)

bcrypt = Bcrypt(app)
jwt = JWTManager(app)
db = Database()

# Middleware for database connection
@app.before_request
def before_request():
    if not hasattr(request, 'db'):
        request.db = db.get_connection()
        request.cursor = request.db.cursor(dictionary=True)

@app.teardown_request
def teardown_request(exception):
    cursor = getattr(request, 'cursor', None)
    if cursor is not None:
        cursor.close()
    db_conn = getattr(request, 'db', None)
    if db_conn is not None:
        db_conn.close()

# Add basic route for testing
@app.route('/')
def index():
    return jsonify({"message": "Welcome to the House Rental API"}), 200

# Error handling
@app.errorhandler(404)
def not_found_error(error):
    return jsonify({
        "error": "Resource not found",
        "message": "The requested URL was not found on the server"
    }), 404

@app.errorhandler(Exception)
def handle_error(error):
    return jsonify({
        "error": str(error),
        "message": "An internal error occurred"
    }), 500

# Authentication routes
@app.route('/api/v1/auth/register', methods=['POST', 'OPTIONS'])

def register():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No input data provided"}), 400
            
        required_fields = ['email', 'first_name', 'last_name', 'phone', 'identity_number']
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400
        
        # Check if user already exists
        request.cursor.execute("SELECT tenant_id FROM tenants WHERE email = %s", (data['email'],))
        if request.cursor.fetchone():
            return jsonify({"error": "Email already registered"}), 400
        
        # Create new user
        user_id = UserModel.create_user(request.cursor, data)
        request.db.commit()
        
        # Generate token
        access_token = create_access_token(identity=user_id)
        
        return jsonify({
            "message": "Registration successful",
            "token": access_token,
            "user_id": user_id
        }), 201
    except Exception as e:
        request.db.rollback()
        return jsonify({"error": str(e)}), 400

@app.route('/api/v1/auth/login', methods=['POST', 'OPTIONS'])

def login():
    try:
        data = request.get_json()
        if not data or 'email' not in data:
            return jsonify({"error": "Email is required"}), 400
            
        request.cursor.execute(
            "SELECT tenant_id, email FROM tenants WHERE email = %s", 
            (data['email'],)
        )
        user = request.cursor.fetchone()
        
        if user:
            access_token = create_access_token(identity=user['tenant_id'])
            return jsonify({
                "message": "Login successful",
                "token": access_token,
                "user": user
            })
        return jsonify({"error": "Invalid credentials"}), 401
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Property routes
@app.route('/api/v1/properties', methods=['GET', 'OPTIONS'])

def get_properties():
    try:
        # Add query parameters for filtering
        filters = {}
        if request.args.get('city'):
            filters['city'] = request.args.get('city')
        if request.args.get('property_type'):
            filters['property_type'] = request.args.get('property_type')
        
        properties = PropertyModel.get_all_properties(request.cursor, filters)
        return jsonify({
            "message": "Properties retrieved successfully",
            "data": properties
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/api/v1/properties', methods=['POST', 'OPTIONS'])

@jwt_required()
def create_property():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No input data provided"}), 400
            
        required_fields = ['property_name', 'address', 'city', 'property_type', 'monthly_rent']
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400
        
        property_id = PropertyModel.create_property(request.cursor, data)
        request.db.commit()
        
        return jsonify({
            "message": "Property created successfully",
            "property_id": property_id
        }), 201
    except Exception as e:
        request.db.rollback()
        return jsonify({"error": str(e)}), 400

# Maintenance request routes
@app.route('/api/v1/maintenance', methods=['POST', 'OPTIONS'])

@jwt_required()
def create_maintenance_request():
    try:
        tenant_id = get_jwt_identity()
        data = request.get_json()
        
        if not data or 'property_id' not in data or 'issue_type' not in data or 'description' not in data:
            return jsonify({"error": "Missing required fields"}), 400
        
        sql = """INSERT INTO maintenance_requests 
                (property_id, tenant_id, issue_type, description, priority, status) 
                VALUES (%s, %s, %s, %s, %s, %s)"""
        values = (
            data['property_id'],
            tenant_id,
            data['issue_type'],
            data['description'],
            data.get('priority', 'Medium'),
            'Pending'
        )
        
        request.cursor.execute(sql, values)
        request.db.commit()
        
        return jsonify({
            "message": "Maintenance request created successfully",
            "request_id": request.cursor.lastrowid
        }), 201
    except Exception as e:
        request.db.rollback()
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=Config.DEBUG, host='0.0.0.0', port=8000)
