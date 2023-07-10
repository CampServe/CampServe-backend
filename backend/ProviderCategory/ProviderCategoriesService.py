from flask_cors import CORS
from flask import jsonify, Blueprint, request
from ProviderCategory.ProviderCategoriesModel import ProviderCategories
from sqlalchemy import func
from Providers.ProviderModel import Providers
from Ratings.RatingsModel import Ratings
from sqlalchemy import and_


provider_categories_route = Blueprint("provider_categories_route", __name__)
CORS(provider_categories_route)


# @provider_categories_route.route("/get_all_services", methods=['GET'])
# def get_services():
#     from app import session

#     # SQL query to fetch the provider IDs with non-null no_of_stars
#     rated_providers_query = session.query(Ratings.provider_id).filter(Ratings.no_of_stars.isnot(None)).distinct().subquery()
#     #rated_providers_query = session.query(Ratings.provider_id).filter(Ratings.no_of_stars.isnot(None)).distinct().subquery()

#     # Fetch all services with joined provider and category information
#     data = session.query(
#         Providers.provider_id,
#         Providers.user_id,
#         Providers.provider_contact,
#         Providers.business_name,
#         Providers.bio,
#         ProviderCategories.main_categories,
#         ProviderCategories.sub_categories,
#         ProviderCategories.subcategories_description,
#         ProviderCategories.subcategory_image,
#         Ratings.no_of_stars
#     ).join(ProviderCategories, Providers.user_id == ProviderCategories.user_id)\
#      .outerjoin(Ratings, and_(Providers.provider_id == Ratings.provider_id, ProviderCategories.sub_categories == Ratings.subcategory))\
#      .join(rated_providers_query, Providers.provider_id == rated_providers_query.c.provider_id, isouter=True)\
#      .group_by(
#         Providers.provider_id,
#         Providers.user_id,
#         Providers.provider_contact,
#         Providers.business_name,
#         Providers.bio,
#         ProviderCategories.main_categories,
#         ProviderCategories.sub_categories,
#         ProviderCategories.subcategories_description,
#         ProviderCategories.subcategory_image,
#         Ratings.no_of_stars
#     ).all()

#     result = {
#         'data': {}
#     }

#     for provider_id, user_id, provider_contact, business_name, bio, main_categories, sub_categories, subcategories_description, subcategory_image, no_of_stars in data:
#         if provider_id not in result['data']:
#             result['data'][provider_id] = {
#                 'provider_id': provider_id,
#                 'user_id': user_id,
#                 'provider_contact': provider_contact,
#                 'business_name': business_name,
#                 'bio': bio,
#                 'main_categories': main_categories,
#                 'subcategories': {},
#             }
#         if sub_categories not in result['data'][provider_id]['subcategories']:
#             result['data'][provider_id]['subcategories'][sub_categories] = {
#                 'subcategories_description': subcategories_description,
#                 'subcategory_image': subcategory_image,
#                 'no_of_stars': [] if no_of_stars is None else [no_of_stars]
#             }
#         else:
#             if no_of_stars is not None:
#                 result['data'][provider_id]['subcategories'][sub_categories]['no_of_stars'].append(no_of_stars)

#     return jsonify(result)


@provider_categories_route.route("/get_all_services", methods=['GET'])
def get_services():
    from app import session

    # SQL query to fetch the provider IDs with non-null no_of_stars
    rated_providers_query = session.query(Ratings.provider_id).filter(Ratings.no_of_stars.isnot(None)).distinct().subquery()

    # Fetch all services with joined provider and category information
    data = session.query(
        Providers.provider_id,
        Providers.user_id,
        Providers.provider_contact,
        Providers.business_name,
        Providers.bio,
        ProviderCategories.main_categories,
        ProviderCategories.sub_categories,
        ProviderCategories.subcategories_description,
        ProviderCategories.subcategory_image,
        func.array_agg(Ratings.no_of_stars).label('ratings')
    ).join(ProviderCategories, Providers.user_id == ProviderCategories.user_id)\
     .join(rated_providers_query, Providers.provider_id == rated_providers_query.c.provider_id, isouter=True)\
     .outerjoin(Ratings, Providers.provider_id == Ratings.provider_id)\
     .group_by(
        Providers.provider_id,
        Providers.user_id,
        Providers.provider_contact,
        Providers.business_name,
        Providers.bio,
        ProviderCategories.main_categories,
        ProviderCategories.sub_categories,
        ProviderCategories.subcategories_description,
        ProviderCategories.subcategory_image,
    ).all()

    result = {
        'data': [
            {
                'provider_id': provider_id,
                'user_id': user_id,
                'provider_contact': provider_contact,
                'business_name': business_name,
                'bio': bio,
                'main_categories': main_categories,
                'sub_categories': sub_categories,
                'subcategories_description': subcategories_description,
                'subcategory_image': subcategory_image,
                'no_of_stars': [] if ratings is None else ratings
            }
            for provider_id, user_id, provider_contact, business_name, bio, main_categories, sub_categories, subcategories_description, subcategory_image, ratings in data
        ]
    }

    return jsonify(result)




