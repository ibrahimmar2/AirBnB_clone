import json
import os.path
import os
from models.base_model import BaseModel
from models.user import User
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models.state import State
from models.city import City

class FileStorage:
    

    __file_path = "file.json"
    __objects = {}
    
    def all(self):
        """Returns the dictionary __objects"""
        return FileStorage.__objects


    def new(self, obj):
        """Sets in __objects the obj with key <obj class name>.id"""
        key = f"{obj.__class__.__name__}.{obj.id}"        
        FileStorage.__objects[key] = obj
    
    def save(self):
        """Serializes __objects to the JSON file (path: __file_path)"""
        odi = FileStorage.__objects
        objdict = {obj: odi[obj].to_dict() for obj in odi.keys()}

        with open(FileStorage.__file_path, "w") as Flie:
            json.dump(objdict, Flie) 
    
    def reload(self):
        """Deserializes the JSON file to __objects"""
        
        if os.path.isfile(FileStorage.__file_path):
            with open(FileStorage.__file_path, "r", encoding="utf-8") as Flie:
                try:
                    obj_dict = json.load(Flie)

                    for key, value in obj_dict.items():
                        class_name, obj_id = key.split('.')

                        cls = eval(class_name)

                        instance = cls(**value)

                        FileStorage.__objects[key] = instance
                except Exception:
                    pass