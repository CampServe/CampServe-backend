import uuid
from flask import jsonify, Blueprint, request, session
import requests
from flask_cors import CORS
import base64
from requests.auth import HTTPBasicAuth



payment_route = Blueprint("payment_route", __name__)
CORS(payment_route)


@payment_route.route('/send_money', methods=['POST'])
def send_money():
    mobile_number = request.json['mobile_number']

    url = f"https://consumer-smrmapi.hubtel.com/request-money"
    username = "xkgfwoxa"
    password = "baiuytlj"

    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Basic ' + base64.b64encode(f'{username}:{password}'.encode()).decode()
    }

    payload = {
    "amount": 1.00,
    "title": "Testing",
    "description": "Testing",
    "clientReference": "731",
    "callbackUrl": "https://webhook.site/a16f5ccd-2916-4904-90e4-0cc455ce105e",
    "cancellationUrl": "http://example.com",
    "returnUrl": "http://example.com",
}

    try:
        res = requests.post(f"{url}/{mobile_number}", headers=headers, json=payload, auth=HTTPBasicAuth(username,password))
        return jsonify(res.text)
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Error occurred: {e}"})
        
