import uuid
from flask import jsonify, Blueprint, request, session
import requests
from flask_cors import CORS
import base64
from requests.auth import HTTPBasicAuth
from Requests.RequestsModel import Requests
from Transactions.TransactionModel import Transactions


# when a request is marked as complete, a pay button is shown on the users side whcih triggers the aylink url
# it means i have to know which request was marked as complete so that i store it next to the request
# and when users click the pay button, they are directed to that link                                

payment_route = Blueprint("payment_route", __name__)
CORS(payment_route)


@payment_route.route('/request_money', methods=['POST'])
def request_money():
    from app import session

    data = request.get_json()
    request_id = data.get('request_id')
    mobile_number = data.get('mobile_number')


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
        response_data = res.json()
        paylink_url = response_data['data']['paylinkUrl']
        id =  paylink_url.split("/")
        paylinkid = id[-1]

        if paylink_url:
            request_row = session.query(Transactions).filter_by(request_id=request_id).first()
        if request_row:
            request_row.paylink = paylink_url
            request_row.paylinkid=paylinkid
            session.commit()
        return jsonify({"paylink": paylink_url, "paylinkid": paylinkid})

    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Error occurred: {e}"})


@payment_route.route('/pay_money', methods=['POST'])
def pay_money():
    from app import session

    data = request.get_json()
    request_id = data.get('request_id')
    recepient_number = data.get('recepient_number')

    try: 
       request_row = session.query(Transactions).filter_by(request_id=request_id).first()
       if request_row:
           request_row.recepient_number = recepient_number
           #when the callback is received, has_paid changes to true
           request_row.has_paid = True
           session.commit()
           
           return jsonify("payment successful")

    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Error occurred: {e}"})