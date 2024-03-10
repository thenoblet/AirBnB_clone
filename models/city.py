#!/usr/bin/python3


"""
This module defines the City class.

The City class represents a city with attributes for the
state ID and city name.
It is a subclass of the BaseModel class, providing common functionality for
managing and storing instances.
"""

from models.base_model import BaseModel


class City(BaseModel):
    """
    City class represents a city with attributes for the
    state ID and city name.

    Attributes:
    - state_id (str): The identifier of the state to which the city belongs.
    - name (str): The name of the city.
    """
    state_id = ""
    name = ""
