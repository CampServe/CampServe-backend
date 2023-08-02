import uuid
from flask import jsonify, Blueprint, request
import requests
from flask_cors import CORS
import base64
from requests.auth import HTTPBasicAuth
from Requests.RequestsModel import Requests
from Transactions.TransactionModel import Transactions
from Providers.ProviderModel import Providers
from Users.UserModel import User
from Transactions.TransactionModel import Transactions


                              

payment_route = Blueprint("payment_route", __name__)
CORS(payment_route)


@payment_route.route('/request_money', methods=['POST'])
def request_money():
    from app import session

    data = request.get_json()
    request_id = data.get('request_id')
    mobile_number = data.get('mobile_number')

    req = session.query(Requests).filter_by(request_id=request_id).first()
    if not req:
        return jsonify({"error": "Request not found."})

    provider_id = req.provider_id
    subcategory = req.subcategory
    user_id = req.user_id
    agreed_price = float(req.agreed_price.replace('GH¢', '').strip())

    provider=session.query(Providers).filter_by(provider_id=provider_id).first()
    business_name = provider.business_name

    url = f"https://consumer-smrmapi.hubtel.com/request-money"
    username = "xkgfwoxa"
    password = "baiuytlj"

    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Basic ' + base64.b64encode(f'{username}:{password}'.encode()).decode()
    }

    payload = {
    "amount": 1.00,
    "title": "CampServe",
    "description": "CampServe",
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
             transaction = Transactions(
                request_id=request_id,
                provider_id=provider_id,
                user_id=user_id,
                amount=agreed_price,
                paylink=paylink_url,
                recepient_number=mobile_number,
                paylinkid=paylinkid,
                subcategory=subcategory,
                business_name=business_name,
                has_paid=False
            )
        session.add(transaction)
        session.commit()
      
        return jsonify({"message": "success","paylink": paylink_url})

    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Error occurred: {e}"})



@payment_route.route('/check_payment', methods=['POST'])
def check_payment():
    from app import session as s
    payload = request.get_json()

    paylink_id = payload['Data']['PaylinkId']

    
    transaction = s.query(Transactions).filter_by(paylinkid=paylink_id).first()

    if not transaction:
        return jsonify({'error': 'No matching transaction found'})


    if transaction.paylinkid == paylink_id:
        transaction.has_paid = True
        s.commit()

    return jsonify({'message': 'payment successful'})




@payment_route.route('/all_user_transactions', methods=['POST'])
def all_transactions():
    from app import session as s
    data = request.get_json()
    user_id = data.get('user_id')

    try:
        transactions = s.query(Transactions).filter_by(user_id=user_id).all()

        transaction_details = []

        for transaction in transactions:
            request_id = transaction.request_id
            paylink = transaction.paylink,
            transaction_id=transaction.transaction_id,
            amount = transaction.amount
            has_paid = transaction.has_paid
            subcategory=transaction.subcategory


            request_data = s.query(Requests).filter_by(request_id=request_id).first()
            provider_id = request_data.provider_id

            provider = s.query(Providers).filter_by(provider_id=provider_id).first()
            business_name = provider.business_name

            transaction_detail = {
                'request_id': request_id,
                'paylink': paylink[0],
                'amount': amount,
                'has_paid': has_paid,
                'provider_business_name': business_name,
                'subcategory':subcategory,
                'transaction_id': transaction_id[0]
            }

            transaction_details.append(transaction_detail)

        return jsonify({'transactions': transaction_details})

    except Exception as e:
        return jsonify({'error': str(e)})



@payment_route.route('/all_provider_transactions', methods=['POST'])
def provider_transactions():
    from app import session as s
    data = request.get_json()
    provider_id = data.get('provider_id')

    try:
        transactions = s.query(Transactions).filter_by(provider_id=provider_id).all()

        transaction_details = []

        for transaction in transactions:
            request_id = transaction.request_id,
            transaction_id=transaction.transaction_id,
            user_id =transaction.user_id
            paylink = transaction.paylink
            amount = transaction.amount
            has_paid = transaction.has_paid
            subcategory=transaction.subcategory


            request_data = s.query(Requests).filter_by(request_id=request_id).first()
            provider_id = request_data.provider_id

            provider = s.query(Providers).filter_by(provider_id=provider_id).first()
            business_name = provider.business_name

            user_data = s.query(User).filter_by(user_id=user_id).first()
            first_name = user_data.first_name,
            last_name=user_data.last_name

            transaction_detail = {
                'request_id': request_id[0],
                'paylink': paylink,
                'amount': amount,
                'has_paid': has_paid,
                'provider_business_name': business_name,
                'subcategory':subcategory,
                'first_name': first_name[0],
                'last_name': last_name
            }

            transaction_details.append(transaction_detail)

        return jsonify({'transactions': transaction_details})

    except Exception as e:
        return jsonify({'error': str(e)})