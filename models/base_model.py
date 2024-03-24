#!/usr/bin/python3
"""
Module for the BaseModel class.
"""
import uuid
from datetime import datetime
import models


class BaseModel:
    def __init__(self, *args, **kwargs):
        TimeFormat = "%Y-%m-%dT%H:%M:%S.%f"
        self.id = str(uuid.uuid4())
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

        if kwargs:
            for k, val in kwargs.items():
                if k == "__class__":
                    continue
                elif k == "created_at" or k == "updated_at":
                    setattr(self, k, datetime.strptime(val, TimeFormat))
                else:
                    setattr(self, k, val)

        models.storage.new(self)

    def save(self):
        """

        """
        self.updated_at = datetime.utcnow()
        models.storage.save()

    def to_dict(self):
        """

        """
        inst_dict = self.__dict__.copy()
        inst_dict["__class__"] = self.__class__.__name__
        inst_dict["created_at"] = self.created_at.isoformat()
        inst_dict["updated_at"] = self.updated_at.isoformat()

        return inst_dict

    def __str__(self):
        """

        """
        ClassName = self.__class__.__name__
        return "[{}] ({}) {}".format(ClassName, self.id, self.__dict__)


if __name__ == "__main__":
    MyModel = BaseModel()
    MyModel.name = "My_First_Model"
    MyModel.my_number = 89
    print(MyModel.id)
    print(MyModel)
    print(type(MyModel.created_at))
    print("--")
    my_model_json = MyModel.to_dict()
    print(my_model_json)
    print("JSON of my_model:")
    for key in my_model_json.keys():
        print("\t{}: ({}) - {}".format(key, type(my_model_json[key]), my_model_json[key]))

    print("--")
    my_new_model = BaseModel(**my_model_json)
    print(my_new_model.id)
    print(my_new_model)
    print(type(my_new_model.created_at))

    print("--")
    print(MyModel is my_new_model)
