from flask import Flask, request, jsonify
from transaction import Transaction
from database import Database
from conversion import Conversion
from transfer import Transfer

app = Flask(__name__)

@app.get("/")
def home():
    return "Welcome to my intership assignment!"

@app.get("/transactions")
def transaction_list():
    values = Database.get_transactions()

    transactions = {}
    transaction_list = []
    for t in values:
        transaction = {}
        transaction['Transaction ID'] = t[0]
        transaction['Amount in BTC'] = float(t[1])
        transaction['Spent'] = t[2]
        transaction['Time of creation'] = t[3]
        transaction_list.append(transaction)
    transactions["Transactions"] = transaction_list

    return jsonify(transactions), 200

@app.get("/balance")
def balance():
    amount_in_BTC = Database.get_BTC_balance()
    amount_in_EUR = Conversion.get_BTC_value_in_EUR(amount_in_BTC)
    balance = {
        "BTC" : amount_in_BTC,
        "EUR" : amount_in_EUR
    }
    return jsonify(balance), 200

@app.post("/transfer")
def transfer():
    data = request.get_json()
    if data["EUR"]:
        transfer = Transfer(Conversion.get_EUR_value_in_BTC(float(data["EUR"])))
        if transfer.validate_transfer():
            transfer.make_transfer()
            return {}, 201
        else:
            return {}, 422
    else:
        return {}, 400

if __name__ == "__main__":
    app.run()