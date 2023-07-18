from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

import os

from dotenv import load_dotenv
load_dotenv()

# Create a new client and connect to the server
client = MongoClient(os.getenv('URI'), server_api=ServerApi('1'))

db = client['new_market']

col_stocks = db['stocks']

col_offers = db['offers']
col_orders = db['orders']

col_users  = db['users']
col_market = db['market']

# STOCKS = [stock['_id'] for stock in col_stocks.find()]