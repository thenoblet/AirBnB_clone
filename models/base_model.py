#!/usr/bin/python3

"""
Module: BaseModel

This module defines the BaseModel class, which serves as a base class
for other models.
It includes functionalities for generating unique identifiers,
managing timestamps, and converting instances to dictionary
representations.

Classes:
- BaseModel: The base model class with common attributes and
  methods for other models.

Usage:
1. Create an instance of BaseModel with a unique identifier and
   optional timestamp values.
2. Utilize the provided methods for string representation, saving updates,
    and converting the instance to a dictionary format.

"""


from uuid import uuid4
from datetime import datetime
import models


class BaseModel:
    """
        The BaseModel class serves as the base class for other models,
        providing common attributes and methods.

        Public instance attributes:
        - id: string - a unique identifier generated using uuid.uuid4()
        - created_at: datetime - timestamp for when the instance is created
        - updated_at: datetime - timestamp for the last update to the instance

        Public instance methods:
        - save(): updates the updated_at attribute with the current datetime
        - to_dict(): returns a dictionary representation of the instance
        - __str__(): returns a string representation of the instance
    """

    def __init__(self, *args, **kwargs):
        """
        Constructor for the BaseModel class.

        Args:
        - *args: Unused
        - **kwargs: Dictionary containing attribute names and values.
        """
        if kwargs:
            # Populate attributes from dictionary representation
            for key, value in kwargs.items():
                if key in ["created_at", "updated_at"]:
                    # Convert datetime strings to datetime objects
                    setattr(
                            self, key, datetime.strptime(
                                value, '%Y-%m-%dT%H:%M:%S.%f'))
                elif key != "__class__":
                    setattr(self, key, value)
        else:
            # Create new instance with unique id and created_at
            self.id = str(uuid4())
            self.created_at = datetime.now()
            self.updated_at = self.created_at
            models.storage.new(self)

    def __str__(self):
        """
        String representation of the BaseModel instance.

        Returns:
        str: A formatted string containing the class name, id,
             and dictionary representation.
        """
        return f"[{self.__class__.__name__}] ({self.id}) {self.__dict__}"

    def save(self):
        """
        Update the 'updated_at' attribute to the current timestamp.
        """
        self.updated_at = datetime.now()

        models.storage.save()

    def to_dict(self):
        """
        Convert the BaseModel instance to a dictionary.

        Returns:
        dict: A dictionary representation of the BaseModel instance.
        """
        model_dict = self.__dict__.copy()

        model_dict["__class__"] = self.__class__.__name__
        model_dict["updated_at"] = self.updated_at.isoformat()
        model_dict["created_at"] = self.created_at.isoformat()

        return model_dict
