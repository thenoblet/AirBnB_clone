#!/usr/bin/python3

"""
This module contains comprehensive unit tests
for the BaseModel class.
"""

import unittest
from datetime import datetime
import json
import os
import sys
import uuid

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from models import storage
from models.base_model import BaseModel


class TestBaseModel(unittest.TestCase):
    """
    Unit tests for the BaseModel class.
    """

    def setUp(self):
        """
        Set up test fixtures.
        """
        self.base_model_1 = BaseModel()
        self.base_model_2 = BaseModel()

    def tearDown(self):
        """
        Clean up test fixtures.
        """
        del self.base_model_1
        del self.base_model_2
        try:
            os.remove("file.json")
        except FileNotFoundError:
            pass

    def test_docstrings(self):
        """
        Test that docstrings are present for the class and its methods.
        """
        self.assertIsNotNone(BaseModel.__doc__)
        self.assertIsNotNone(BaseModel.__init__.__doc__)
        self.assertIsNotNone(BaseModel.__str__.__doc__)
        self.assertIsNotNone(BaseModel.save.__doc__)
        self.assertIsNotNone(BaseModel.to_dict.__doc__)

    def test_class_has_docstring(self):
        """
        Test that the class itself has a docstring.
        """
        self.assertIsNotNone(BaseModel.__doc__)

    def test_str_return_value(self):
        """
        Test that the __str__ method returns the expected string representation.
        """
        expected_output = f"[BaseModel] ({self.base_model_1.id}) {self.base_model_1.__dict__}"
        self.assertEqual(str(self.base_model_1), expected_output)

    def test_unique_ids(self):
        """
        Test that two instances of BaseModel have different IDs.
        """
        self.assertNotEqual(self.base_model_1.id, self.base_model_2.id)

    def test_updated_at_updated(self):
        """
        Test that the 'updated_at' attribute is updated on calling the 'save' method.
        """
        initial_time = self.base_model_1.updated_at
        self.base_model_1.save()
        self.assertNotEqual(initial_time, self.base_model_1.updated_at)

    def test_to_dict_iso_format(self):
        """
        Test that the to_dict method returns a dictionary with ISO-formatted date strings.
        """
        model_dict = self.base_model_1.to_dict()
        self.assertEqual(model_dict['__class__'], 'BaseModel')
        self.assertIsInstance(model_dict['updated_at'], str)
        self.assertIsInstance(model_dict['created_at'], str)

    def test_attribute_data_types(self):
        """
        Test that the data types of attributes are as expected.
        """
        self.assertIsInstance(self.base_model_1.updated_at, datetime)
        self.assertIsInstance(self.base_model_1.created_at, datetime)
        self.assertIsInstance(self.base_model_1.id, str)

    def test_different_uuids(self):
        """
        Test that two instances of BaseModel have different UUIDs.
        """
        self.assertNotEqual(self.base_model_1.id, self.base_model_2.id)

    def test_nonexistent_attribute_method(self):
        """
        Test that accessing a nonexistent attribute or method raises an AttributeError.
        """
        with self.assertRaises(AttributeError):
            getattr(self.base_model_1, 'nonexistent_attr')
        with self.assertRaises(AttributeError):
            getattr(self.base_model_1, 'nonexistent_method')()

    def test_created_updated_same_time(self):
        """
        Test that 'created_at' and 'updated_at' are the same initially.
        """
        self.assertEqual(
                self.base_model_1.created_at, self.base_model_1.updated_at)

    def test_instantiation_from_dict(self):
        """
        Test instantiation of a BaseModel instance from a dictionary representation.
        """
        model_dict = self.base_model_1.to_dict()
        new_model = BaseModel(**model_dict)
        self.assertEqual(new_model.to_dict(), model_dict)

    def test_class_name_in_to_dict(self):
        """
        Test that the class name is included in the dictionary representation.
        """
        model_dict = self.base_model_1.to_dict()
        self.assertIn('__class__', model_dict)
        self.assertEqual(model_dict['__class__'], 'BaseModel')

    def test_type_error_to_dict(self):
        """
        Test that calling to_dict with an argument other than None raises a TypeError.
        """
        with self.assertRaises(TypeError):
            self.base_model_1.to_dict(123)

    def test_same_uuid_datetime_from_dict(self):
        """
        Test that a BaseModel instance created from its dictionary representation
        has the same UUID and datetime values.
        """
        model_dict = self.base_model_1.to_dict()
        new_model = BaseModel(**model_dict)
        self.assertEqual(new_model.id, self.base_model_1.id)
        self.assertEqual(new_model.created_at, self.base_model_1.created_at)

    def test_invalid_date_instantiation_from_dict(self):
        """
        Test that instantiation from a dictionary with an invalid date format
        raises a ValueError.
        """
        model_dict = self.base_model_1.to_dict()
        model_dict['created_at'] = 'invalid_date_format'
        with self.assertRaises(ValueError):
            BaseModel(**model_dict)

    def test_updated_created_data_types_from_dict(self):
        """
        Test that the 'updated_at' and 'created_at' attributes are datetime
        objects after instantiation
        """
        model_dict = self.base_model_1.to_dict()
        new_model = BaseModel(**model_dict)
        self.assertIsInstance(new_model.updated_at, datetime)
        self.assertIsInstance(new_model.created_at, datetime)

    def test_iso_dates_in_dict(self):
        """Test datetime format"""
        model_dict = self.base_model_1.to_dict()
        self.assertTrue(isinstance(model_dict['updated_at'], str) and isinstance(model_dict['created_at'], str))

    def test_to_dict_returns_dict(self):
        """
        Test that the to_dict method returns a dictionary.
        """
        self.assertIsInstance(self.base_model_1.to_dict(), dict)

    def test_type_error_save(self):
        """
        Test that calling the save method with an argument other than None raises a TypeError.
        """
        with self.assertRaises(TypeError):
            self.base_model_1.save(123)

    def test_json_file_created_on_save(self):
        """
        Test that a JSON file is created upon calling the save method.
        """
        self.assertFalse(os.path.exists("file.json"))
        self.base_model_1.save()
        self.assertTrue(os.path.exists("file.json"))

    def test_storage_instance_type(self):
        """
        Test that the stored instances in the JSON file are of type dict.
        """
        self.base_model_1.save()
        with open("file.json", 'r') as file:
            data = json.load(file)
            for key in data.keys():
                self.assertIsInstance(data[key], dict)

    def test_updated_at_updated_on_save(self):
        """
        Test that the 'updated_at' attribute is updated upon calling the save method.
        """
        initial_time = self.base_model_1.updated_at
        self.base_model_1.save()
        self.assertNotEqual(initial_time, self.base_model_1.updated_at)



class Test_BaseModel(unittest.TestCase):
    """
    Test cases for the BaseModel class.
    """

    def test_setUp(self):
        """
        Test the setUp method, ensuring 'file.json' is removed.
        """
        try:
            os.remove("file.json")
        except:
            pass

    def test_tearDown(self):
        """
        Test the tearDown method, ensuring 'file.json' is removed.
        """
        try:
            os.remove("file.json")
        except:
            pass

    def test_docstring(self):
        """
        Test that docstrings are present for key methods in the BaseModel class.
        """
        self.assertTrue(len(BaseModel.__doc__) > 1)
        self.assertTrue(len(BaseModel.__init__.__doc__) > 1)
        self.assertTrue(len(BaseModel.__str__.__doc__) > 1)
        self.assertTrue(len(BaseModel.save.__doc__) > 1)
        self.assertTrue(len(BaseModel.to_dict.__doc__) > 1)

    def test_isinstance(self):
        """
        Test that an instance of BaseModel is of type BaseModel.
        """
        obj = BaseModel()
        self.assertIsInstance(obj, BaseModel)

    def test_id_v4_uuid(self):
        """
        Test that the id attribute of BaseModel is a version 4 UUID.
        """
        obj = BaseModel()
        test_uuid = uuid.UUID(obj.id, version=4)
        self.assertEqual(str(test_uuid), obj.id, "Error: Different version")

    def test_args(self):
        """
        Test that BaseModel instantiation with an argument doesn't add an attribute.
        """
        b = BaseModel(8)
        self.assertEqual(type(b).__name__, "BaseModel")
        self.assertFalse(hasattr(b, "8"))

    def test_str(self):
        """
        Test the string representation of BaseModel.
        """
        b = BaseModel()
        printb = b.__str__()
        self.assertEqual(printb,
                         "[BaseModel] ({}) {}".format(b.id, b.__dict__))

    def test_save(self):
        """
        Test the save method, checking for file creation and attribute updates.
        """
        obj = BaseModel()
        obj.save()
        key = "BaseModel.{}".format(obj.id)
        comp = storage._FileStorage__objects[key]
        self.assertEqual(obj.id, comp.id)
        self.assertTrue(os.path.isfile("file.json"))
        self.assertNotEqual(obj.created_at, obj.updated_at)

    def test_to_dict(self):
        """
        Test the to_dict method, ensuring the correct dictionary representation is returned.
        """
        obj = BaseModel()
        new_dict = obj.__dict__.copy()
        new_dict["__class__"] = obj.__class__.__name__
        new_dict["created_at"] = new_dict["created_at"].isoformat()
        new_dict["updated_at"] = new_dict["updated_at"].isoformat()
        comparing = obj.to_dict()
        self.assertDictEqual(new_dict, comparing)

if __name__ == '__main__':
    unittest.main()
