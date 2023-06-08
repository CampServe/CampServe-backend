from flask_cors import CORS
from flask import jsonify, Blueprint, request, session
from Students.StudentModel import Students
from werkzeug.security import generate_password_hash, check_password_hash
from Users.UserModel import User
import jwt
from datetime import datetime, timedelta
from functools import wraps


users_route = Blueprint("users_route", __name__)
CORS(users_route)


@users_route.route("/add_user", methods=['POST'])
def add_user():
    from app import session as s
    first_name = request.json['first_name']
    last_name = request.json['last_name']
    username = request.json['username']
    password = request.json['password']

    if 'email' in session:
        user_email = session['email']

    hashed_password = generate_password_hash(password)

    check_username = s.query(User).filter_by(username=username).first()
    if check_username:
        result = {
            'status': 'user already exists'
        }

    else:
        user = User(first_name=first_name, last_name=last_name, username=username,
                    password=hashed_password, email=user_email, is_service_provider=False)
        s.add(user)
        s.commit()

        result = {
            'status': 'User created'
        }
    return jsonify(result)


@users_route.route("/user_login", methods=['POST'])
def login():
    from app import session
    from app import app
    username = request.json['username']
    password = request.json['password']

    user = session.query(User).filter_by(username=username).first()
    if user:
        verify = check_password_hash(pwhash=user.password, password=password)
        if verify:

            #generate token
            token = jwt.encode({
                'status': 'Login successful',
                'username': user.username,
                'user_id': user.user_id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'is_service_provider': user.is_service_provider,
                'account_type': 'regular user',
                'expiration': str(datetime.utcnow() + timedelta(days=1))
            },
                app.config['SECRET_KEY'])

            result = {
                'token': token
            }

            return jsonify(result)
        else:
            result = 'Incorrect username or password'
            return jsonify(result)
    else:
        # Check if the username exists in the database
        existing_user = session.query(
            User).filter_by(username=username).first()
        if existing_user:
            result = 'Incorrect password'
        else:
            result = 'Incorrect credentials'
        return jsonify(result)


# @users_route.route("/check_token", methods=['GET'])
# def protected_route():
#     from app import app

#     #Token is passed in the 'token' header
#     token = request.headers.get('token')  
    
#     if token is None:
#         return jsonify({'message': 'Unauthorized'}), 401

#     # Token validation
#     try:
#         user = jwt.decode(token, app.config['SECRET_KEY'])
#     except jwt.InvalidTokenError:
#         return jsonify({'message': 'Invalid token'}), 401

#     # Token expiration check
#     expiration = datetime.strptime(user['expiration'], "%Y-%m-%d %H:%M:%S.%f")
#     if expiration < datetime.utcnow():
#         return jsonify({'message': 'Token expired'}), 401

   
#     # Proceed with regular application flow for an authenticated user
#     result = {
#         'message': 'Access granted',
#         'username': user['username'],
#         'user_id': user['user_id'],
#         'first_name': user['first_name'],
#         'last_name': user['last_name'],
#         'email': user['email'],
#         'is_service_provider': user['is_service_provider'],
#         'account_type': user['account_type']

#     }

#     return jsonify(result)