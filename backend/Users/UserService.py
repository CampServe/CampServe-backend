from flask_cors import CORS
from flask import jsonify, Blueprint, request
from Students.StudentModel import Students
from werkzeug.security import generate_password_hash, check_password_hash

from Users.UserModel import User


users_route = Blueprint("users_route", __name__)
CORS(users_route)

@users_route.route("/add_user",methods=['POST'])
def add_user():
    from app import session
    first_name = request.json['first_name']
    last_name = request.json['last_name']
    username = request.json['username']
    password = request.json['password']
    email = request.json['email']
    ref_number = request.json['ref_number']
    
    hashed_password = generate_password_hash(password)


    user = User(first_name=first_name, last_name=last_name, username=username, password=hashed_password,email=email,ref_number=ref_number)
    session.add(user)
    session.commit()

    result = {
        'status': 'User created'
    }
    return jsonify(result)


@users_route.route("/user_login",methods=['POST'])
def login():
    from app import session
    username = request.json['username']
    password = request.json['password']
    
    user = session.query(User).filter_by(username=username).first()
    if user:
        verify = check_password_hash(pwhash=user.password, password=password)
        if verify:
            result = {
                'status': 'Login successful'
            }
            return jsonify(result)
        else:
            result = 'Incorrect username or password'
            return jsonify(result)
    else:
        result = 'Username does not exist'
        return jsonify(result)


