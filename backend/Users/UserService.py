from lib2to3.pgen2 import token
from flask_cors import CORS
from flask import jsonify, Blueprint, request,session,current_app
from Students.StudentModel import Students
from werkzeug.security import generate_password_hash, check_password_hash
from Users.UserModel import User


users_route = Blueprint("users_route", __name__)
CORS(users_route)

@users_route.route("/add_user",methods=['POST'])
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
        user = User(first_name=first_name, last_name=last_name, username=username, password=hashed_password,email=user_email,is_service_provider=False)
        s.add(user)
        s.commit()

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
                'status': 'Login successful',
                'first_name': user.first_name,
                'last_name': user.last_name,
                'username': user.username,
                'email': user.email,
                'user_id':user.user_id,
                'is_service_provider': user.is_service_provider
            }

            #this is where you generate the token. the token will have information on who the user is and what to send back
            return jsonify(result)
        else:
            result = 'Incorrect username or password'
            return jsonify(result)
    else:
        # Check if the username exists in the database
        existing_user = session.query(User).filter_by(username=username).first()
        if existing_user:
            result = 'Incorrect password'
        else:
            result = 'Incorrect credentials'
        return jsonify(result)





