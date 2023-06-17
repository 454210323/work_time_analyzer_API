from decimal import Decimal

class Item:
    def __init__(self, item_id, item_name, amount):
        self.item_id:str = item_id
        self.item_name:str = item_name
        self.amount:Decimal = amount

    def to_dict(self):
        return {
            "item_id": self.item_id,
            "item_name": self.item_name,
            "amount": self.amount
        }