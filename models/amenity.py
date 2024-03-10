#!/usr/bin/python3

"""
This module defines the Amenity class.

The Amenity class represents an amenity with a name attribute.
"""

from models.base_model import BaseModel


class Amenity(BaseModel):
    name = ""
