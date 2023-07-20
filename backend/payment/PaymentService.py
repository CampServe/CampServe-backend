import uuid
from flask import jsonify, Blueprint, request, session
import requests
from flask_cors import CORS
import base64
from requests.auth import HTTPBasicAuth
from hubtel import Hubtel




payment_route = Blueprint("payment_route", __name__)
CORS(payment_route)

class Hubtel:
    def __init__(self,username,password,merchantId):
        self.base_url = "https://api.hubtel.com/v1/merchantaccount/"
        self.username = username
        self.password = password
        self.merchant_id = merchantId
        usrPass = "{0}:{1}".format(self.username,self.password)
        auth_byte = usrPass.encode('utf-8')
        self.basic = str(base64.b64encode(auth_byte))[2:-1]
        self.headers = {'Authorization': 'Basic {0}'.format(self.basic)}
        self.items = []
        print(self.basic)


@payment_route.route("/send_money", methods=['POST'])
def send():
        #name = request.json['name']
        #number = request.json['number']
        #email = request.json['email']
        #amount = request.json['amount']
        
        base_url = "https://devp-reqsendmoney-230622-api.hubtel.com/request-money/0206436575"
        payload = {
            "PrimaryCallbackUrl": "https://webhook.site/a16f5ccd-2916-4904-90e4-0cc455ce105e"
        }

        headers = {
            'Content-Type': 'application/json',
        }
        try:
            r = requests.post(base_url, headers=headers, data=payload)
            return r.json()
        except Exception as e:
            print(e)