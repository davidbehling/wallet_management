from tinydb import TinyDB
import os

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'database_db.json')
DB_PATH = os.path.abspath(DB_PATH)

db = TinyDB(DB_PATH)
wallets_table = db.table('coldwallets')
dest_table = db.table('fromwallets')
trans_table = db.table('transactions')
price_table = db.table('crypto_prices')