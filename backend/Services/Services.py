from crypt import methods
from flask import jsonify, Blueprint, request
from flask_cors import CORS



services_route = Blueprint("services_route", __name__)
CORS(services_route)



@services_route.route('/book_services', methods=['POST'])
def book_services():
    pass