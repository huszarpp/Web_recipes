import uuid
from src.common.database import Database


class Ingredients(object):

    def __init__(self, ingredient, quantity, unit, food_id, _id=None):
        self._id = uuid.uuid4().hex if _id is None else _id
        self.ingredient = ingredient
        self.quantity = quantity
        self.unit = unit
        self.food_id = food_id

    def save_ingredient(self):
        Database.insert(collection='ingredients',
                        data=self.json()
                        )

    def json(self):
        return {
            '_id': self._id,
            'ingredient': self.ingredient,
            'quantity': self.quantity,
            'unit': self.unit,
            'food_id': self.food_id
        }

    @staticmethod
    def find_ingredients_by_food_id(food_id):
        ingredients = [item for item in Database.find(collection='ingredients',
                                                      query={'food_id': food_id}
                                                      )
                       ]
        return [Ingredients(**item) for item in ingredients]

    @staticmethod
    def find_all_ingredients():
        ingredients = [item for item in Database.find(collection='ingredients',
                                                      query={}
                                                      )
                       ]
        return [Ingredients(**item) for item in ingredients]

    @staticmethod
    def delete_ingredient(food_id):
        Database.delete_many(collection='ingredients',
                             query={'food_id': food_id}
                             )
