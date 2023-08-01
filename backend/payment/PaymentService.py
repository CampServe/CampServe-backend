import uuid
from flask import jsonify, Blueprint, request, session
import requests
from flask_cors import CORS
import base64
from requests.auth import HTTPBasicAuth
from Requests.RequestsModel import Requests
from Transactions.TransactionModel import Transactions
from Providers.ProviderModel import Providers
from Users.UserModel import User


                              

payment_route = Blueprint("payment_route", __name__)
CORS(payment_route)


@payment_route.route('/request_money', methods=['POST'])
def request_money():
    from app import session

    data = request.get_json()
    request_id = data.get('request_id')
    mobile_number = data.get('mobile_number')

    req = session.query(Requests).filter_by(request_id=request_id).first()
    agreed_price = float(req.agreed_price.replace('GH¢', '').strip())

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
    "callbackUrl": "https://campserve-server.onrender.com/check_payment",
    "cancellationUrl": "http://example.com",
    "returnUrl": "http://example.com",
}

    try:
        res = requests.post(f"{url}/{mobile_number}", headers=headers, json=payload, auth=HTTPBasicAuth(username,password))
        response_data = res.json()
        paylink_url = response_data['data']['paylinkUrl']
        id =  paylink_url.split("/")
        paylinkid = id[-1]

        if paylink_url:
            request_row = session.query(Transactions).filter_by(request_id=request_id).first()
        if request_row:
            request_row.paylink = paylink_url
            request_row.recepient_number = mobile_number
            request_row.paylinkid=paylinkid
            session.commit()
        return jsonify({"paylink": paylink_url, "paylinkid": paylinkid})

    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Error occurred: {e}"})



@payment_route.route('/check_payment', methods=['POST'])
def check_payment():
    # Assuming your payload is available in the request data, you can extract it like this:
    payload = request.get_json()

    # Make a request to your callback URL with a POST request
    callback_url = payload.get("callbackUrl")
    if callback_url:
        response = requests.post(callback_url, json=payload)
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Print the response content
            print(response.json())
        else:
            # If the request failed, print an error message
            print(f"Request to callback URL failed with status code: {response.status_code}")
    else:
        print("Callback URL is not provided in the payload.")
    
    # You can return a response here if needed, such as an acknowledgment message
    return "Payment status check initiated"


@payment_route.route('/all_user_transactions', methods=['GET'])
def all_transactions():
    from app import session as s
    data = request.get_json()
    user_id = data.get('user_id')

    try:
        transactions = s.query(Transactions).filter_by(user_id=user_id).all()

        transaction_details = []

        for transaction in transactions:
            request_id = transaction.request_id
            paylink = transaction.paylink
            amount = transaction.amount
            has_paid = transaction.has_paid

            user = s.query(User).filter_by(user_id=user_id).first()
            first_name = user.first_name
            last_name = user.last_name

            request_data = s.query(Requests).filter_by(request_id=request_id).first()
            provider_id = request_data.provider_id

            provider = s.query(Providers).filter_by(provider_id=provider_id).first()
            business_name = provider.business_name

            transaction_detail = {
                'request_id': request_id,
                'paylink': paylink,
                'amount': amount,
                'has_paid': has_paid,
                'provider_business_name': business_name
            }

            transaction_details.append(transaction_detail)

        return jsonify({'transactions': transaction_details})

    except Exception as e:
        return jsonify({'error': str(e)})