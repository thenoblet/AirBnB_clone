#!/usr/bin/python3

""" This module defines the Review class. """

from models.base_model import BaseModel


class Review(BaseModel):
    """
    Review class represents a review with attributes for the place ID,
    user ID, and text.

    Attributes:
    - place_id (str): The identifier of the place being reviewed.
    - user_id (str): The identifier of the user who wrote the review.
    - text (str): The text content of the review.
    """
    place_id = ""
    user_id = ""
    text = ""
