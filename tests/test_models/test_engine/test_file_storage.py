#!/usr/bin/python3


"""Unittest cases for file storage"""


import unittest
from models.engine.file_storage import FileStorage
from models.base_model import BaseModel
from models import storage
import os
import json


class Test_File_Storage(unittest.TestCase):
    """
    Class for testing File storage class.
    """

    def setUp(self):
        """SetUps tests"""
        self.storage = FileStorage()

    def resetStorage(self):
        """Resets FileStorage data."""
        FileStorage._FileStorage__objects = {}
        if os.path.isfile(FileStorage._FileStorage__file_path):
            os.remove(FileStorage._FileStorage__file_path)

    def tearDown(self):
        """Tears down test methods."""
        self.resetStorage()
        pass

    def test_docstring(self):
        """Checks if docstring exists"""
        self.assertTrue(len(FileStorage.__doc__) > 1)
        self.assertTrue(len(FileStorage.all.__doc__) > 1)
        self.assertTrue(len(FileStorage.new.__doc__) > 1)
        self.assertTrue(len(FileStorage.save.__doc__) > 1)
        self.assertTrue(len(FileStorage.reload.__doc__) > 1)

    def test_instantiation(self):
        """Tests instantiation of storage class."""
        self.assertEqual(type(storage).__name__, "FileStorage")

    def test_isinstance(self):
        """"Test if is an instance of the class"""
        obj = FileStorage()
        self.assertIsInstance(obj, FileStorage)

    def test_save(self):
        """Testing the save function"""
        obj = BaseModel()
        self.assertIsInstance(obj, BaseModel)
        self.storage.new(obj)
        self.storage.save()
        self.assertTrue(self.storage._FileStorage__file_path)
        self.assertTrue(self.storage._FileStorage__objects)
        self.assertTrue(os.path.isfile(self.storage._FileStorage__file_path))
        key = "BaseModel.{}".format(obj.id)
        self.storage._FileStorage__objects = {}
        self.storage.reload()
        self.assertDictEqual(self.storage.all()[key].to_dict(), obj.to_dict())

    def test_all_method_return_type(self):
        """Tests the return type of the `all()` method."""
        self.assertTrue(isinstance(storage.all(), dict))

    def test_key_name_in_obj_dict_same_objects(self) -> None:
        """Ensure key names are correct for two objects of the same class."""
        base1 = BaseModel()
        base2 = BaseModel()

        expected_key_1 = f"{base1.__class__.__name__}.{base1.id}"
        expected_key_2 = f"{base2.__class__.__name__}.{base2.id}"

        self.assertDictEqual(
            {expected_key_1: base1, expected_key_2: base2}, storage.all())

    def test_5_attributes(self):
        """Tests class attributes."""
        self.resetStorage()
        self.assertTrue(hasattr(FileStorage, "_FileStorage__file_path"))
        self.assertTrue(hasattr(FileStorage, "_FileStorage__objects"))
        self.assertEqual(getattr(FileStorage, "_FileStorage__objects"), {})


class TestFileStorageMethods(unittest.TestCase):

    def setUp(self):
        # Set up the initial state for each test
        self.file_path = "test_file.json"
        FileStorage._FileStorage__file_path = self.file_path
        self.storage = FileStorage()

    def tearDown(self):
        # Clean up after each test
        if os.path.exists(self.file_path):
            os.remove(self.file_path)

    def test_new_adding_object(self):
        # Test adding a new object
        obj = BaseModel()
        self.storage.new(obj)
        result = self.storage.all()
        expected_key = "BaseModel." + obj.id
        self.assertIn(expected_key, result)
        self.assertEqual(result[expected_key], obj)

    def test_new_overwriting_object(self):
        # Test overwriting an existing object
        obj1 = BaseModel()
        obj2 = BaseModel()
        self.storage.new(obj1)
        self.storage.new(obj2)
        result = self.storage.all()
        expected_key = "BaseModel." + obj2.id
        self.assertIn(expected_key, result)
        self.assertEqual(result[expected_key], obj2)

    def test_save_non_empty_storage(self):
        # Test save method with non-empty storage
        obj = BaseModel()
        self.storage.new(obj)
        self.storage.save()
        with open(self.file_path, "r") as file:
            content = json.load(file)
        expected_content = {
                f"BaseModel.{obj.id}": obj.to_dict() for obj in self.storage.all().values()}
        self.assertEqual(content, expected_content)

    def test_reload_invalid_json_format(self):
        # Test reload method with an invalid JSON file
        with open(self.file_path, "w") as file:
            file.write("invalid json format")
        with self.assertRaises(json.JSONDecodeError):
            self.storage.reload()

    def test_file_path_modification(self):
        # Test handling of file path modification
        new_file_path = "new_test_file.json"
        FileStorage._FileStorage__file_path = new_file_path
        self.storage.new(BaseModel())
        self.storage.save()
        self.assertTrue(os.path.exists(new_file_path))


if __name__ == '__main__':
    unittest.main()
