from flask_cors import CORS
from flask import jsonify, Blueprint, request
from Students.StudentModel import Students
from werkzeug.security import check_password_hash
from Providers.ProviderModel import Providers
from Users.UserModel import User
from ProviderCategory.ProviderCategoriesModel import ProviderCategories




providers_route = Blueprint("providers_route", __name__)
CORS(providers_route)


@providers_route.route("/signup_as_provider/<user_id>", methods=['POST'])
def sign_up(user_id):
    from app import session

    #getting the selected categories from a provider
    data = request.get_json()

    #provider information when signing up
    provider_contact = request.json['provider_contact']
    bio = request.json['bio']
    business_name = request.json['business_name']

    #using the user id to change the provider status
    user = session.query(User).filter_by(user_id=user_id).first()
    user.is_service_provider = True
    session.commit()

    #updating the provider info
    provider = session.query(Providers).filter_by(user_id=user_id).first()

    if provider:
        # Update existing provider
        provider.provider_contact = provider_contact
        provider.bio = bio
        provider.business_name = business_name
    else:
        # Create new provider
        provider = Providers(
            user_id=user_id,
            provider_contact=provider_contact,
            bio=bio,
            business_name=business_name
        )
        session.add(provider)
    session.commit()

    #looping through the categories
    selected_categories = data['selectedSubcategories']

    
    for category in selected_categories:
        category_name = category['category']
        subcategories = category['subcategory']

        for subcategory in subcategories:
            categories = ProviderCategories(user_id=user_id, main_categories=category_name, sub_categories=subcategory)
            session.add(categories)

    session.commit()

    result = {
        'status': 'Provider created with credentials'
    }


    return jsonify(result)


@providers_route.route("/login_as_provider", methods=['POST'])
def provider_login():
    from app import session
    username = request.json['username']
    password = request.json['password']

# Find the user in the users table
    user = session.query(User).filter_by(username=username).first()

    if user:
        # Check if the user is also a provider
        provider = session.query(Providers).filter_by(user_id=user.user_id).first()

        if provider:
            # Verify the password
            if check_password_hash(user.password, password):
                # User is authenticated as a provider

                result = {
                    'status': 'Provider login successful',
                    'user_id': user.user_id,
                    'username': username
                }
                return jsonify(result)
            else:
                result = {
                    'status': 'Invalid username or password'
                }
        else:
            result = {
                'status': 'User is not a provider'
            }
    else:
        result = {
            'status': 'User not found'
        }

    return jsonify(result)



