from flask import Flask, request, jsonify
from database import Database
from conversion import Conversion
from transaction import Transaction
from transfer import Transfer

app = Flask(__name__)

@app.get("/")
def home():
    return "Welcome to my intership assignment!"

@app.get("/transactions") #get transactions
def transaction_list():
    transactions = Database.get_converted_transactions()
    return jsonify(transactions), 200

@app.get("/balance") #get balance in btc and eur
def balance():
    amount_in_BTC = Database.get_BTC_balance()
    if amount_in_BTC:
        amount_in_EUR = Conversion.get_BTC_value_in_EUR(amount_in_BTC)
        balance = {
            "BTC" : amount_in_BTC,
            "EUR" : amount_in_EUR
        }
        return jsonify(balance), 200
    else:
        return jsonify({"Message" : "No transactions"}), 400

@app.post("/transfer") #create new transfer
def transfer():
    try:
        data = request.get_json()
    except:
        return jsonify({"Error" : "Failed to parse body. Need request body in json format"}), 400
    try:
        value = float(next(iter(data.values())))
        transfer = Transfer(Conversion.get_EUR_value_in_BTC(value))
        if transfer.validate_transfer():
            transfer.make_transfer()
            transactions = Database.get_converted_transactions()
            return jsonify(transactions), 201
        else:
            return jsonify({"Message" : "Not enough balance"}), 400
    except:
        return jsonify({"Error" : "Wrong input value"}), 400


@app.post("/data") #add new transactions to the database by providing only amounts in btc via json
def new_data():
    try:
        data = request.get_json()
    except:
        return jsonify({"Error" : "Failed to parse body. Need request body in json format"}), 400
    try:
        for value in iter(data.values()):
            value = float(value)
            transaction = Transaction(value)
            transaction.create_transaction()

        new_transactions = Database.get_converted_transactions()
        return jsonify(new_transactions), 201
    except:
        return jsonify({"Error" : "Wrong input values"}), 400

@app.delete("/data") #delete existing transactions in the database
def delete_data():
    Database.delete_transactions()
    return "", 204

if __name__ == "__main__":
    app.run()
