from secrets import token_hex
import datetime
from database import Database

class Transaction():

    def __init__(self, amount):
        self.transaction_id = token_hex(16)
        self.amount = amount
        self.spent = False
        self.created_at = datetime.datetime.now()

    def create_transaction(self):
        Database.create_transaction((self.transaction_id, self.amount, self.spent, self.created_at))