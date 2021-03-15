import uuid
from src.common.database import Database


class Types_Of_Food(object):

    def __init__(self, type, _id=None):
        self._id = uuid.uuid4().hex if _id is None else _id
        self.type = type

    def save_type(self):
        Database.insert(collection='types_of_food',
                        data=self.json()
                        )

    def json(self):
        return {
            '_id': self._id,
            'type': self.type
        }

    @staticmethod
    def find_one_id(t_id):
        one_type = Database.find_one(collection='types_of_food',
                                     query={'_id': t_id}
                                     )
        if one_type == None:
            return None
        else:
            return Types_Of_Food(one_type['type'], one_type['_id'])

    @staticmethod
    def find_one_type(type):
        one_type = Database.find_one(collection='types_of_food',
                                     query={'type': type}
                                     )
        if one_type == None:
            return None
        else:
            return Types_Of_Food(one_type['type'], one_type['_id'])

    @staticmethod
    def find_all_types():
        all_types = [item for item in Database.find(collection='types_of_food',
                                                    query={}
                                                    )
                     ]
        return [Types_Of_Food(**item) for item in all_types]

    def get_id(self):
        return self._id

    @staticmethod
    def type_exists(type_name):
        return Types_Of_Food.find_one_type(type=type_name) != None
