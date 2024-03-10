#!/usr/bin/python3

"""
This module defines the State class.

The State class represents a state with a name attribute.
It is a subclass of the BaseModel class, providing common
functionality for managing and storing instances.
"""

from models.base_model import BaseModel


class State(BaseModel):
    """
    State class represents a state with a name attribute.

    Attributes:
    - name (str): The name of the state.
    """
    name = ""
