import requests
import json
import base64

message = "2z7ta7s9nk194392ai2ze595trufw5knwlk9um2g0rzs2.apps.vivapayments.com:gdKC2ef2agez3kWv162O647Y0tD0nB"
message_bytes = message.encode('ascii')
base64_bytes = base64.b64encode(message_bytes)
base64_message = base64_bytes.decode('ascii')

print(base64_message)
## Request Access Token:


headers = {
    'Authorization': 'Basic %s'%base64_message,
}

data = {
    'grant_type': 'client_credentials',
}

response = requests.post('https://demo-accounts.vivapayments.com/connect/token', headers=headers, data=data)
print (response.text)
accesss_token = json.loads(response.text).get('access_token')


import requests
headers = {
    'Authorization': 'Bearer %s'%accesss_token,
}

json_data = {
    'amount': 1000,
    'customerTrns': 'Short description of purchased items/services to display to your customer',
    'customer': {
        'email': 'johdoe@vivawallet.com',
        'fullName': 'John Doe',
        'phone': '+30999999999',
        'countryCode': 'GB',
        'requestLang': 'en-GB',
    },
    'paymentTimeout': 300,
    'preauth': False,
    'allowRecurring': False,
    'maxInstallments': 12,
    'paymentNotification': True,
    'tipAmount': 100,
    'disableExactAmount': False,
    'disableCash': True,
    'disableWallet': True,
    'sourceCode': '6092',
    'merchantTrns': 'Short description of items/services purchased by customer',
    'tags': [
        'tags for grouping and filtering the transactions',
        'this tag can be searched on VivaWallet sales dashboard',
        'Sample tag 1',
        'Sample tag 2',
        'Anoteher string',
    ],
}

response = requests.post('https://demo-api.vivapayments.com/checkout/v2/orders', headers=headers, json=json_data)
orderCode = json.loads(response.text).get('orderCode')
URL = "https://demo.vivapayments.com/web/checkout?ref=%s"%orderCode
print (URL)
