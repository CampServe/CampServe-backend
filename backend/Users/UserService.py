import email
from flask_cors import CORS
from flask import jsonify, Blueprint, request, session
from Students.StudentModel import Students
from werkzeug.security import generate_password_hash, check_password_hash
from Users.UserModel import User
import jwt
from datetime import datetime, timedelta
from Providers.ProviderModel import Providers


users_route = Blueprint("users_route", __name__)
CORS(users_route)


revoked_tokens = set()


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
    check_email = s.query(User).filter_by(email=user_email).first()
    if check_username:
        result = {
            'status': 'user already exists'
        }

    elif check_email:
        result = {
            'status': 'user with that email already exists'
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

            # generate token
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


@users_route.route('/logout', methods=['POST'])
def logout():
    try:
        # print(revoked_tokens)
        token = request.headers.get('Authorization')

        # Check if the token is revoked
        if token in revoked_tokens:
            return jsonify({'message': 'Token has already been revoked'})

        # Add the token to the revoked token set
        revoked_tokens.add(token)
        # print(revoked_tokens)

        return jsonify({'message': 'Logout successful'})
    except Exception as e:
        return jsonify({'message': 'Logout failed', 'error': str(e)})


@users_route.route('/switch_to_provider', methods=['GET'])
def switch_to_provider():
    from app import session
    from app import app

    token = request.headers.get('Authorization')
    if not token:
        return jsonify({'message': 'Token is missing'})

    try:
        decoded_token = jwt.decode(token, app.config['SECRET_KEY'])
        user_id = decoded_token['user_id']

        user = session.query(User).get(user_id)
        provider = session.query(Providers).filter_by(user_id=user_id).first()
    

        result = {
            'user_id': user.user_id,
            'username': user.username,
            'business_name': provider.business_name,
            'bio': provider.bio,
            'provider_contact': provider.provider_contact,
            'account_type': 'provider',
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email
        }

        return jsonify(result)

    except jwt.ExpiredSignatureError:
        return jsonify({'message': 'Token has expired'})
    except jwt.InvalidTokenError:
        return jsonify({'message': 'Invalid token'})
