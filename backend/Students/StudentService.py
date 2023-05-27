from flask_cors import CORS
from flask import jsonify, Blueprint, request
from Students.StudentModel import Students
from werkzeug.security import generate_password_hash, check_password_hash


students_route = Blueprint("students_route", __name__)
CORS(students_route)


@students_route.route("/hash", methods=['POST'])
def hash_password():
    from app import session
    username = request.json['username']
    password = request.json['password']

    student = session.query(Students).filter_by(username=username).first()
    if student:
        hashed_password = generate_password_hash(password)
        student.password = hashed_password

    try:
        session.commit()
        result = {'status': 'Password hashed and stored successfully'}

    except Exception as e:
        session.rollback()
        result = {'status': 'Error occurred while hashing the password'}

    return jsonify(result)


@students_route.route("/login", methods=['POST'])
def student_login():
    from app import session
    username = request.json['username']
    password = request.json['password']

    student = session.query(Students).filter_by(username=username).first()

    if student:
        verify = check_password_hash(pwhash=student.password, password=password)
        if verify:
            result = {
                'student_id': student.student_id,
                'status': 'Login successful'
            }
            return jsonify(result)
        else:
            result = {
                'status': 'Incorrect username or password'
            }
            return jsonify(result)
    else:
        result = {
            'status': 'Username does not exist'
        }
        return jsonify(result)

