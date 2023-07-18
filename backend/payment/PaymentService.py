import uuid
from flask import jsonify, Blueprint, request, session
import requests
from flask_cors import CORS
import base64



payment_route = Blueprint("payment_route", __name__)
CORS(payment_route)

# username = 'ifbflmpd'
# password = 'zcdaruuy'
# endpoint = 'https://devp-reqsendmoney-230622-api.hubtel.com/send-money'

# headers = {
#     'Content-Type': 'application/json',
# }

# req_body = {
#     "amount": 1,
#     "title": "Payment for a transaction",
#     "description": "Payment for a transaction",
#     "clientReference": "8791789731",
#     "callbackUrl": "https://webhook.site/dc52dcf3-b978-4b6a-b16e-3394e014a140",
#     "cancellationUrl": "http://example.com",
#     "returnUrl": "http://example.com",
# }

@payment_route.route('/send_payment', methods=['POST'])
def send_payment_request():
    mobile_number = '0501334031'
    hubtel_base_url = 'https://devp-reqsendmoney-230622-api.hubtel.com'
    endpoint = f"{hubtel_base_url}/send-money/{mobile_number}"

    username = 'ifbflmpd'
    password = 'zcdaruuy'

    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Basic ' + base64.b64encode(f"{username}:{password}".encode()).decode()
    }

    req_body = {
        "amount": 1,
        "title": "string",
        "description": "string",
        "clientReference": str(uuid.uuid4()),
        "callbackUrl": "http://example.com",
        "cancellationUrl": "http://example.com",
        "returnUrl": "http://example.com",
        "logo": "http://example.com"
    }
    
    response = requests.post(endpoint, json=req_body, headers=headers)


    if response.status_code == 200:
        data = response.json()
    else:
        # Handle non-2xx status code (error response)
        data = {'error': f"Error from Hubtel API: {response.text}"}

    return jsonify(data)


