#!/bin/usr/python3

""" Creates a unique FileStorage instance """

from models.engine.file_storage import FileStorage

storage = FileStorage()  # Create a FileStorage instance
storage.reload()
