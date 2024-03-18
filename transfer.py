from database import Database
from transaction import Transaction

class Transfer():

    def __init__(self, amount):
        self.amount = amount

    def validate_transfer(self):
        return self.amount <= Database.get_BTC_balance() or self.amount < 0.00001
    
    def make_transfer(self):
        transactions = Database.get_transactions()
        total = 0
        transactions_spent = []

        for transaction in transactions:
            total += float(transaction[1])
            transactions_spent.append(transaction[0])
            if total > self.amount:
                break

        for transaction_id in transactions_spent:
            Database.transaction_spent(transaction_id)

        new_transaction = Transaction(total - self.amount)
        new_transaction.create_transaction()