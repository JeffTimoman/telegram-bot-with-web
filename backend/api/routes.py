from flask import Blueprint, request, jsonify
from flask_cors import CORS
from backend import db, bcrypt
from backend.models import User
api = Blueprint('api', __name__)
CORS(api, resources={r"/*": {"origins": "*"}})

@api.route('/login', methods=['POST', 'GET'])
def login():
    print(request.get_json())
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    
    if user is None:
        return jsonify({'error': 'Incorrect password or username', 'status': 401}), 401
    
    if not bcrypt.check_password_hash(user.password, data['password']):
        return jsonify({'error': 'Incorrect password or username', 'status': 401}), 401
    
    return jsonify({'status': 200, 'token': "token_louwis"}), 200
    