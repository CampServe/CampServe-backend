from pypaystack2 import Paystack
import json
import ssl
import http.client
from flask import Blueprint, jsonify
from flask_cors import CORS


ssl_context = ssl.create_default_context(
cafile='/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/site-packages/certifi/cacert.pem')


paystack = Paystack(auth_key='sk_test_7c2e2eec657534c8fef2b7fe4c3cb81270e29402')

headers = {
    "Authorization": "Bearer sk_test_7c2e2eec657534c8fef2b7fe4c3cb81270e29402",
    "Content-Type": "application/json"
}


#creating a customer
new_customer = paystack.customers.create(
    email="jeffkwakye17@gmail.com",
    first_name="Jeffrey",
    last_name="Kwakye",
    phone="+233501334031"
)



# Mobile money payments
mobile_money = {
    "email": "jeffkwakye17@gmail.com",
    "amount": "50",
    "currency": "GHS",
    "mobile_money": {
        "phone": "0551234987",
        "provider": "tgo"
    }
}

conn = http.client.HTTPSConnection("api.paystack.co", 443, context=ssl_context)

try:
    payload = json.dumps(mobile_money)

    conn.request("POST", "/charge", payload, headers)

    # get response from server
    res = conn.getresponse()
    # decode response from server
    data = res.read().decode("utf-8")

    print(json.loads(data))
    # d = json.loads(data)
    # print({'status': d['data']['status']})

    conn.close()
except Exception as e:
    print({'message': 'Could not create customer', 'error': str(e)})




# getting a customer
# get_customer = paystack.customers.get_customer(email_or_code="jeffkwakye17@gmail.com")
# print(get_customer)

# new mobile money transaction


# fetching customers
# response = paystack.customers.get_customer(email_or_code="jeffkwakye4u@email.com")
# print(response)


# updating customers
# customer_id = "CUS_knezuwtg54ockiq"
# update_customer = paystack.customers.update(code=customer_id,last_name="test")

# print(update_customer)
