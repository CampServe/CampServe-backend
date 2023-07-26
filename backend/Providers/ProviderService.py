from flask_cors import CORS
from flask import jsonify, Blueprint, request
from werkzeug.security import check_password_hash
from ProviderCategory.ProviderCategoriesModel import ProviderCategories
from Providers.ProviderModel import Providers
from Users.UserModel import User
from sqlalchemy import func,cast, Float,Numeric
from Requests.RequestsModel import Requests
import jwt
from datetime import datetime, timedelta
from Ratings.RatingsModel import Ratings
from Users.UserModel import User
from Providers.ProviderService import Providers
import re





providers_route = Blueprint("providers_route", __name__)
CORS(providers_route)


revoked_tokens = set()



@providers_route.route("/signup_as_provider/<user_id>", methods=['POST'])
def sign_up(user_id):
    from app import session
    from ProviderCategory.ProviderCategoriesModel import ProviderCategories


    # getting the selected categories from a provider
    data = request.get_json()

    # provider information when signing up
    provider_contact = request.json['provider_contact']
    bio = request.json['bio']
    business_name = request.json['business_name']

    # using the user id to change the provider status
    user = session.query(User).filter_by(user_id=user_id).first()
    user.is_service_provider = True
    session.commit()

    # updating the provider info
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

    # looping through the categories
    selected_categories = data['selectedSubcategories']

    for category in selected_categories:
        category_name = category['category']
        subcategories = category['subcategories']

        for subcategory in subcategories:
            subcategory_name = subcategory['name']
            description = subcategory['description']
            subcategory_image = subcategory.get('image') or None

            categories = ProviderCategories(user_id=user_id, main_categories=category_name, sub_categories=subcategory_name, subcategories_description=description, subcategory_image=subcategory_image,number_of_visits=0)
            session.add(categories)

    session.commit()

    result = {
        'status': 'Provider created with credentials'
    }

    return jsonify(result)



@providers_route.route("/login_as_provider", methods=['POST'])
def provider_login():
    from app import session
    from app import app
    from ProviderCategory.ProviderCategoriesModel import ProviderCategories

    username = request.json['username'].lower()
    password = request.json['password']

    # Find the user in the users table
    user = session.query(User).filter_by(username=username).first()


    if user:
        # Check if the user is also a provider
        provider = session.query(Providers).filter_by(
            user_id=user.user_id).first()

        if provider:
            # Verify the password
            if check_password_hash(user.password, password):

                # Retrieve user details from the users table
                user_details = session.query(User).filter_by(user_id=user.user_id).first()

                subcategories = session.query(ProviderCategories).filter_by(user_id=user.user_id).all()
                #we can call the route here
                # generate token
                token = jwt.encode({
                    'status': 'Provider login successful',
                    'user_id': user.user_id,
                    'provider_id': provider.provider_id,
                    'username': user.username,
                    'business_name': provider.business_name,
                    'bio': provider.bio,
                    'provider_contact': provider.provider_contact,
                    'account_type': 'provider',
                    'first_name': user_details.first_name,
                    'last_name': user_details.last_name,
                    'email': user_details.email,
                    'expiration': str(datetime.utcnow() + timedelta(days=1)),
                    'subcategories': [
                        subcategory.sub_categories for subcategory in subcategories
                    ],

                }, app.config['SECRET_KEY'])

                result = {
                    'token': token
                }
            else:
                result = 'Invalid username or password'
        else:
            result = 'User is not a provider'
    else:
        result = 'User not found'

    return jsonify(result)


@providers_route.route('/provider_logout', methods=['POST'])
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


@providers_route.route('/switch_to_user', methods=['GET'])
def switch_to_user():
    from app import session
    from app import app

    token = request.headers.get('Authorization')
    print(token)
    if not token:
        return jsonify({'message': 'Token is missing'})

    try:
        decoded_token = jwt.decode(token, app.secret_key, algorithms=['HS256'])
        user_id = decoded_token['user_id']
        expiration = decoded_token['expiration']

        user = session.query(User).get(user_id)

        token = jwt.encode({
            'username': user.username,
            'user_id': user.user_id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'is_service_provider': user.is_service_provider,
            'account_type': 'regular user',
            'expiration': expiration
        },
            app.secret_key)

        result = {
            'token': token
        }

        return jsonify(result)

    except jwt.ExpiredSignatureError:
        return jsonify({'message': 'Token has expired'})
    except jwt.InvalidTokenError:
        return jsonify({'message': 'Invalid token'})
    except Exception as e:
        print(f"Exception: {e}")
        return jsonify({'message': 'An error occurred'})



@providers_route.route('/get_provider_info', methods=['POST'])
def get_provider_info():
    from app import session
    from ProviderCategory.ProviderCategoriesModel import ProviderCategories


    data = request.get_json()
    provider_id = data['provider_id']

    # Retrieve provider information from the providers table
    provider = session.query(Providers).filter_by(provider_id=provider_id).first()

    if not provider:
        return jsonify({'message': 'Provider not found'})

    # Retrieve ratings for the provider
    ratings = session.query(Ratings).filter_by(provider_id=provider_id).all()

    # Retrieve provider categories using the user_id from the providers table
    provider_categories = session.query(ProviderCategories).filter_by(user_id=provider.user_id).all()

    # Prepare the output dictionary
    output = {
        'business_name': provider.business_name,
        'contact': provider.provider_contact,
        'bio': provider.bio,
        'main_categories': [],
        'sub_categories': []
    }

    # Extract subcategories from provider_categories
    subcategories_dict = {}
    for category in provider_categories:
        subcategories_dict[category.sub_categories] = {
            'subcategory_image': category.subcategory_image,
            'description': category.subcategories_description,
            'request_summary': {
                'pending': 0,
                'in_progress': 0,
                'completed': 0,
                'declined': 0,
                'total_amount_earned': 0
            },
            'rating_details': []
        }
        output['main_categories'].append(category.main_categories)

    # Populate comments, no_of_stars, and rating_details for each subcategory
    for rating in ratings:
        subcategory = rating.subcategory
        if subcategory in subcategories_dict:
            user = session.query(User).filter_by(user_id=rating.user_id).first()
            rating_details = {
                'id': rating.rating_id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'stars': rating.no_of_stars,
                'review': rating.comments,
                'timestamp': rating.timestamp
            }
            subcategories_dict[subcategory]['rating_details'].append(rating_details)

    # Assign subcategories dictionary to the output
    output['sub_categories'] = subcategories_dict


    #Count the requests and calculate the total amount earned for each subcategory
    for subcategory, subcategory_info in subcategories_dict.items():
        pending_count = session.query(func.count(Requests.provider_id)).filter(
            Requests.provider_id == provider_id,
            Requests.subcategory == subcategory,
            Requests.status_acc_dec == 'no action',
            Requests.status_comp_inco == 'no action'
        ).scalar()

        in_progress_count = session.query(func.count(Requests.provider_id)).filter(
            Requests.provider_id == provider_id,
            Requests.subcategory == subcategory,
            Requests.status_acc_dec == 'accepted',
            Requests.status_comp_inco == 'incomplete'
        ).scalar()

        completed_count = session.query(func.count(Requests.provider_id)).filter(
            Requests.provider_id == provider_id,
            Requests.subcategory == subcategory,
            Requests.status_acc_dec == 'accepted',
            Requests.status_comp_inco == 'complete'
        ).scalar()

        declined_count = session.query(func.count(Requests.provider_id)).filter(
            Requests.provider_id == provider_id,
            Requests.subcategory == subcategory,
            Requests.status_acc_dec == 'declined',
            Requests.status_comp_inco == 'no action'
        ).scalar()

        print("Calling session.query with extract_numeric")

        total_amount_earned = session.query(
        func.coalesce(func.sum(func.cast(func.replace(Requests.agreed_price, 'GH¢ ', ''), Numeric)), 0.0)
        ).filter(
        Requests.provider_id == provider_id,
        Requests.subcategory == subcategory,
        Requests.status_acc_dec == 'accepted',
        Requests.status_comp_inco == 'complete'
        ).scalar()


        # Update the request summary for each subcategory in the output dictionary
        subcategory_info['request_summary']['pending'] = pending_count
        subcategory_info['request_summary']['in_progress'] = in_progress_count
        subcategory_info['request_summary']['completed'] = completed_count
        subcategory_info['request_summary']['declined'] = declined_count
        subcategory_info['request_summary']['total_amount_earned'] = total_amount_earned or 0
        # subcategories_dict[subcategory]['request_summary']['total_amount_earned'] = total_amount_earned or 0.0


    return jsonify(output)



@providers_route.route('/update_provider', methods=['POST'])
def update_provider():
    from app import session
    data = request.get_json()

    provider_id = data.get('provider_id')
    user_id = data.get('user_id')
    bio = data.get('bio')
    provider_contact = data.get('provider_contact')
    business_name = data.get('business_name')
    sub_categories = data.get('subcategories')

    if not provider_id or not user_id:
        return jsonify({'message': 'Invalid data provided'})

    # Update the Provider table
    provider = session.query(Providers).filter_by(provider_id=provider_id).first()
    if provider:
        if bio:
            provider.bio = bio
        if provider_contact:
            provider.provider_contact = provider_contact
        if business_name:
            provider.business_name = business_name

    # Update the ProviderCategory table
    if sub_categories:
        provider_category = session.query(ProviderCategories).filter_by(user_id=user_id).first()
        if provider_category:
            sub_categories_data = provider_category.sub_categories

            # Loop through the received sub_categories and update the corresponding records
            for subcategory in sub_categories:
                subcategory_name = list(subcategory.keys())[0]
                subcategory_data = subcategory[subcategory_name]

                if subcategory_name in sub_categories_data:
                    sub_categories_data[subcategory_name]['description'] = subcategory_data.get('description', sub_categories_data[subcategory_name]['description'])
                    sub_categories_data[subcategory_name]['image'] = subcategory_data.get('image', sub_categories_data[subcategory_name]['image'])

            provider_category.sub_categories = sub_categories_data

    session.commit()
    
    return jsonify({'message': 'Data updated successfully'})