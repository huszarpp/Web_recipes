import uuid
from src.common.database import Database


class Food(object):

    def __init__(self, name, preparation, type_id, img=None, _id=None):
        self._id = uuid.uuid4().hex if _id is None else _id
        self.name = name
        self.img = img
        self.preparation = preparation
        self.type_id = type_id

    def save_food(self):
        Database.insert(collection='food',
                        data=self.json()
                        )

    def json(self):
        return {
            '_id': self._id,
            'name': self.name,
            'img': self.img,
            'preparation': self.preparation,
            'type_id': self.type_id
        }

    @staticmethod
    def delete_food(_id):
        Database.delete_one(collection='food',
                            query={'_id': _id}
                            )

    @staticmethod
    def find_one_food_by_name(name):
        data_food = Database.find_one(collection='food',
                                      query={'name': name}
                                      )
        return Food(**data_food)

    @staticmethod
    def find_one_food_by_id(id):
        data_food = Database.find_one(collection='food',
                                      query={'_id': id}
                                      )
        return Food(**data_food)

    @staticmethod
    def find_foods_by_type(t_id):
        foods_list = [item for item in Database.find(collection='food',
                                                     query={'type_id': t_id}
                                                     )
                      ]
        return [Food(**item) for item in foods_list]

    @staticmethod
    def find_foods():
        foods_list = [item for item in Database.find(collection='food',
                                                     query={}
                                                     )
                      ]
        return [Food(**item) for item in foods_list]

    def get_id(self):
        return self._id

    @property
    def id(self):
        return self._id

    @staticmethod
    def food_exists(name):
        food_ex = Database.find_one(collection='food',
                                    query={'name': name}
                                    )
        return food_ex is not None
