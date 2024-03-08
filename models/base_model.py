from uuid import uuid4
from datetime import datetime

class BaseModel:
    def __init__(self):
        """
        Constructor for the BaseModel class.

        Parameters:
        - id (str): Unique identifier generated using uuid4.
        - created_at (datetime): The timestamp representing the creation time.
        - updated_at (datetime): The timestamp representing the last update time.
        """
        self.id = str(uuid4())
        self.created_at = datetime.now()
        self.updated_at = self.created_at


    def __str__(self):
        """
        String representation of the BaseModel instance.

        Returns:
        str: A formatted string containing the class name, id, and dictionary representation.
        
        """
        return f"[{self.__class__.__name__}] ({self.id}) {self.__dict__}"


    def save(self):
        """
        Update the 'updated_at' attribute to the current timestamp.
        """
        self.updated_at = datetime.now()


    def to_dict(self):
        model_dict = self.__dict__.copy()

        model_dict["__class__"] = self.__class__.__name__
        model_dict["updated_at"] = self.updated_at.isoformat()
        model_dict["created_at"] = self.created_at.isoformat()

        return model_dict
