from models.entities.item import Item

class CustomerPurchases:
    def __init__(self, id, name, items):
        self.id:int = id
        self.name:str = name
        self.items:list[Item] = items

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "items": [item.to_dict() for item in self.items]
        }