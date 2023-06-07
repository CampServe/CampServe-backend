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


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        from app import app
        token = None
        # jwt is passed in the request header
        if 'token' in request.headers:
            token = request.headers['token']

        # return message if token is not passed
        if not token:
            return jsonify({'message' : 'Token is missing !!'})
  
        try:
            # decoding the payload to fetch the stored details
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = User.query\
                .filter_by(username = data['username'])\
                .first()
        except:
            return jsonify({
                'message' : 'Token is invalid !!'
            }), 401
        # returns the current logged in users context to the routes
        return  f(current_user, *args, **kwargs)
  
    return decorated

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
                'user': username,
                'user_id': user.user_id,
                'expiration': str(datetime.utcnow() + timedelta(days=1))
            },
                app.config['SECRET_KEY'])

            result = {
                'status': 'Login successful',
                'first_name': user.first_name,
                'last_name': user.last_name,
                'username': user.username,
                'email': user.email,
                'user_id': user.user_id,
                'is_service_provider': user.is_service_provider,
                'account_type': 'regular user',
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



# @users_route.route("/logout", methods=['POST'])
# @token_required
# def logout():
#     # removing the token from local storage or cookies
#     # Assuming the token is stored in local storage
#     if 'token' in request.headers:
#         del request.headers['token']


#     # Send a response indicating successful logout
#     return jsonify({'message': 'Logout successful'})

