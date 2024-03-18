import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()
connection = psycopg2.connect(os.getenv("DATABASE"))
            

class Database:

    def execute_query(query, *args, **kwargs):
        values = kwargs.get('values', None)
        fetch = kwargs.get('fetch', False)
        with connection:
            with connection.cursor() as cursor:
                if (values):
                    cursor.execute(query, values)
                else:
                    cursor.execute(query)
                if fetch:
                    return cursor.fetchall()
            

    def create_transaction(values): 

        INSERT_TRANSACTION = """INSERT INTO transactions
        (transaction_id, amount, spent, transfer_time) VALUES (%s, %s, %s, %s) returning 0"""

        Database.execute_query(INSERT_TRANSACTION, values=values)

    def transaction_spent(id):
        
        TRANSACTION_SPENT = """UPDATE transactions SET spent = true WHERE transaction_id = %s"""

        Database.execute_query(TRANSACTION_SPENT, values=(id,))

    def get_transactions(): 

        SELECT_TRANSACTIONS = """SELECT * FROM transactions;"""

        return Database.execute_query(SELECT_TRANSACTIONS, fetch=True)
    

    def get_BTC_balance():

        SELECT_BALANCE = """SELECT SUM(amount) FROM transactions WHERE spent = false"""

        return float(Database.execute_query(SELECT_BALANCE, fetch=True)[0][0])