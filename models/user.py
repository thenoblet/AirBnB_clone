#!/usr/bin/python3

"""
This module defines the User class.

The User class represents a user with specific attributes such as email,
password, first_name, and last_name.
It is a subclass of the BaseModel class, providing common functionality for
managing and storing instances.
"""

from models.base_model import BaseModel


class User(BaseModel):
    """
    User class represents a user with specific attributes.

    Attributes:
    - email (str): User's email address.
    - password (str): User's password.
    - first_name (str): User's first name.
    - last_name (str): User's last name.
    """

    email = ""
    password = ""
    first_name = ""
    last_name = ""
