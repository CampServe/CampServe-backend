from flask_cors import CORS
from flask import jsonify, Blueprint, request
from ProviderCategory.ProviderCategoriesModel import ProviderCategories

from Providers.ProviderModel import Providers


provider_categories_route = Blueprint("provider_categories_route", __name__)
CORS(provider_categories_route)


@provider_categories_route.route("/get_all_services", methods=['GET'])
def get_services():
    from app import session

    data = session.query(
        Providers.user_id,
        Providers.provider_contact,
        Providers.business_name,
        Providers.bio,
        ProviderCategories.main_categories,
        ProviderCategories.sub_categories
    ).all()

    result = {
        'data': [
            {
                'user_id': user_id,
                'provider_contact': provider_contact,
                'business_name': business_name,
                'bio': bio,
                'main_categories': main_categories,
                'sub_categories': sub_categories

            }
            for user_id,  provider_contact, business_name, bio, main_categories, sub_categories, in data
        ]
    }

    return jsonify(result)
