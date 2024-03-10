#!/usr/bin/python3

import json
from os.path import exists
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class FileStorage:
    """
    FileStorage class manages the serialization and deserialization of objects
    to and from a JSON file.

    Attributes:
    - __file_path (str): Path to the JSON file for storing serialized objects.
    - __objects (dict): Dictionary to store instances of objects.

    Methods:
    - all(self): Returns a dictionary of all objects currently stored.
    - new(self, obj): Adds a new object to the __objects dictionary.
    - save(self): Serializes and saves the current objects to the JSON file.
    - reload(self): Deserializes objects from the JSON file and
      updates __objects.
    """

    __file_path = "file.json"
    __objects = {}
    __models = {
            "BaseModel": BaseModel,
            "User": User,
            "State": State,
            "City": City,
            "Amenity": Amenity,
            "Place": Place,
            "Review": Review
    }

    def all(self):
        """
        Returns a dictionary of all objects currently stored.

        Parameters:
            None

        Returns:
            dict: Dictionary containing all stored objects.
        """
        return self.__objects

    def new(self, obj):
        """
        Adds a new object to the __objects dictionary.

        Parameters:
            obj: The object to be added.

        Returns:
            None
        """
        key = f"{obj.__class__.__name__}.{obj.id}"
        self.__objects[key] = obj

    def save(self):
        """
        Serializes and saves the current objects to the JSON file.

        Parameters:
            None

        Returns:
            None
        """
        serialised_objects = {}

        for key, obj in self.__objects.items():
            serialised_objects[key] = obj.to_dict()

        with open(self.__file_path, "w", encoding="utf-8") as file:
            json.dump(serialised_objects, file, indent=4)

    def reload(self):
        """
        Deserializes objects from the JSON file and updates __objects.

        Parameters:
            None

        Returns:
            None
        """
        if exists(self.__file_path):
            with open(self.__file_path, "r", encoding="utf-8") as file:
                instances = json.load(file)

            for key, obj_dict in instances.items():
                # Extract class name and object id from the key
                class_name, obj_id = key.split(".")

                # Dynamically import the class and create an instance
                """ obj_instance = getattr(
                __import__(class_name), class_name)(**obj_dict) """
                obj_instance = self.__models[class_name](**obj_dict)

                # Update __objects with the new instance
                self.__objects[key] = obj_instance
