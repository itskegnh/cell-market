from mongo import *
from discordio import *

class SyncedDocument:
    def __init__(self, collection, _id):
        self.collection = collection
        self.id = _id
        self.document = {}

    def sync(self):
        self.document = self.collection.find_one({'_id': self.id})
        return self

    def __getattr__(self, name):
        return self.document.get(name)

class Stock(SyncedDocument):
    def __init__(self, _id):
        super().__init__(col_stocks, _id)
        self.image = disnake.File(f'./cells/{self.id}.png', filename=f'{self.id}.png')

class Offer(SyncedDocument):
    def __init__(self, _id):
        super().__init__(col_offers, _id)

class Order(SyncedDocument):
    def __init__(self, _id):
        super().__init__(col_orders, _id)

STOCKS = [Stock(stock.get('_id')) for stock in col_stocks.find({})]