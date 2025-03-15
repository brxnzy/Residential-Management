from flask import Flask, render_template, jsonify, request
import paypalrestsdk
import json
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


paypalrestsdk.configure({
    "mode": "sandbox",  # sandbox or live
    "client_id": "AZG-ukIFcrgMo5_Ep7g9olBovjNHUMKb9takI2YVjLAtiFjUwBKJAbEwvnaKq-U6vKZchyQhYANhfMUD",
    "client_secret": "EMDPOWfoiQ_k994-5h17yyYeUZxx7VX6-3C_6Y3mwzXlGBdH_YWdUrYDtoFTfn04j7XCoEHDgPnXNPtw"
})

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/payment', methods=['POST'])
def payment():
    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal"},
        "redirect_urls": {
            "return_url": "http://127.0.0.1:5000/execute",
            "cancel_url": "http://127.0.0.1:5000/"
        },
        "transactions": [{
            "item_list": {
                "items": [{
                    "name": "testitem",
                    "sku": "12345",
                    "price": "500.00",
                    "currency": "USD",
                    "quantity": 1}]
            },
            "amount": {
                "total": "500.00",
                "currency": "USD"
            },
            "description": "This is the payment transaction description."
        }]
    })

    if payment.create():
        print('Payment success!')
    else:
        print(json.dumps(payment.error, indent=4))

    return jsonify({'paymentID': payment.id})

@app.route('/execute', methods=['POST'])
def execute():
    success = False
    payment = paypalrestsdk.Payment.find(request.form['paymentID'])

    if payment.execute({'payer_id': request.form['payerID']}):
        print('Execute success!')
        success = True
    else:
        print(json.dumps(payment.error, indent=4))

    return jsonify({'success': success})

if __name__ == '__main__':
    app.run(debug=True)
