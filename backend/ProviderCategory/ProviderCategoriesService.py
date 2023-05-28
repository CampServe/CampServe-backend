from flask_cors import CORS
from flask import jsonify, Blueprint, request


provider_categories_route = Blueprint("provider_categories_route", __name__)
CORS(provider_categories_route)


#2 routs
#1. to return all the main categories associated with a particular student id
#2. to return all the sub categories associated with a particular student id