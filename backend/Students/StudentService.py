from flask_cors import CORS
from flask import jsonify, Blueprint, request
from Students.StudentModel import Students
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
from Students.otp_service import generate_otp, save_otp, retrieve_otp, clear_otp, send_otp_email
from flask import session


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


@students_route.route("/student_verification", methods=['POST'])
def student_verification():
    email = request.json['email']
    
    otp = generate_otp()

    otp_expiration = datetime.datetime.now() + datetime.timedelta(hours=1)

    save_otp(email, otp, otp_expiration)

    send_otp_email(email, otp)

    result = {
        'status': 'OTP sent to email',
        'email': email
    }

    return jsonify(result)


@students_route.route("/otp_verification", methods=['POST'])
def student_email_verification():
    email = request.json['email']
    otp = request.json['otp']

    stored_otp, otp_expiration = retrieve_otp(email)

    if stored_otp:
        if otp == stored_otp and datetime.datetime.now() <= otp_expiration:
            clear_otp(email)

            session['email'] = email


            result = {
                'status': 'Email verification successful',
                'email': email
            }

        else:
            result = {
                'status': 'Invalid OTP or OTP expired'
            }
    else:
        result = {
            'status': 'Email not found'
        }

    return jsonify(result)
