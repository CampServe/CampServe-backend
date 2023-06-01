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
    
    hashed_password = generate_password_hash(password)


    user = User(first_name=first_name, last_name=last_name, username=username, password=hashed_password)
    session.add(user)
    session.commit()

    result = {
        'status': 'User created'
    }
    return jsonify(result)

