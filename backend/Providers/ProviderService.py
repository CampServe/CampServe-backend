from crypt import methods
from flask_cors import CORS
from flask import jsonify, Blueprint, request
from Students.StudentModel import Students
from werkzeug.security import check_password_hash
from Providers.ProviderModel import Providers


providers_route = Blueprint("providers_route", __name__)
CORS(providers_route)


@providers_route.route("/signup_as_provider", methods=['POST'])
def sign_up():
    from app import session
    username = request.json['username']
    ref_number = request.json['ref_number']
    password = request.json['password']

    student = session.query(Students).filter_by(username=username).first()
    if student and ref_number and check_password_hash(pwhash=student.password, password=password):

        provider = Providers(student_id=student.student_id)
        session.add(provider)
        session.commit()

        result = {
            'student_id': student.student_id,
            'status': 'sign up successful'
        }

    else:
        result = {
            'status': 'The user name, password or studentid provided is incorrect.'}

    return jsonify(result)


@providers_route.route("/login_as_provider", methods=['POST'])
def provider_login():
    from app import session
    username = request.json['username']
    password = request.json['password']

    student = session.query(Students).filter_by(username=username).first()
    if student:
        verify = check_password_hash(pwhash=student.password, password=password)
        if verify:
            result = {
                'student_id': student.student_id,
                # 'status': 'Login successful'
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


@providers_route.route("/check_if_provider/<student_id>", methods=['POST'])
def check_if_provider(student_id):
    from app import session
    provider = session.query(Providers).filter_by(student_id=student_id).first()

    if provider:
        return jsonify({'message': 'provider found'})
    else:
        return jsonify({'message': 'provider not found'})


@providers_route.route("/update_provider_data/<student_id>", methods=['POST'])
def update_provider_data(student_id):
    from app import session

    provider = session.query(Providers).filter_by(student_id=student_id).first()
    # if provider:

    provider_contact = request.json['contact']
    profile_pic = request.json['picture']
    bio = request.json['bio']
    banner_image = request.json['banner_image']
    business_name = request.json['business_name']

    provider.provider_contact = provider_contact
    provider.profile_pic = profile_pic
    provider.bio = bio
    provider.banner_image = banner_image
    provider.business_name = business_name


    #create the provider categories object here and merge them. so it identifies which provider and commits it to the 
    #provider categories table.so with every selection it identifies which student selected and it is put into the database on different
    #rows because of database normalisation. I want to use the student_id to populate the databse since its a foreign key


    session.commit()
    return jsonify({'message': 'Provider data updated successfully.'})


# @providers_route.route("/login_as_provider", methods=['POST'])
# def provider_login():
#     from app import session
#     username = request.json['username']
#     password = request.json['password']

#     provider_contact = request.json['contact']
#     profile_pic = request.json['picture']
#     bio = request.json['bio']
#     banner_image = request.json['banner_image']
#     business_name = request.json['business_name']

#     student = session.query(Students).filter_by(username=username).first()
#     if student and check_password_hash(student.password, password):
#         #call that logic
#         provider = session.query(Providers).filter_by(student_id=student.student_id).first()
#         if provider:

#             provider.provider_contact = provider_contact
#             provider.profile_pic = profile_pic
#             provider.bio = bio
#             provider.banner_image = banner_image
#             provider.business_name = business_name


#             session.commit()
#             return jsonify({'message': 'Provider data updated successfully.'})
#         else:
#             return jsonify({'message': 'Provider not found for the given student ID.'})
#     else:
#         return jsonify({'message': 'Invalid username or password.'})
