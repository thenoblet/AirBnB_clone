#!/usr/bin/python3

import unittest
from datetime import datetime
import json
import os
from models.base_model import BaseModel
from models import storage


class TestBaseModel(unittest.TestCase):

    def setUp(self):
        self.base_model_1 = BaseModel()
        self.base_model_2 = BaseModel()

    def tearDown(self):
        del self.base_model_1
        del self.base_model_2
        try:
            os.remove("file.json")
        except FileNotFoundError:
            pass

    def test_docstrings(self):
        self.assertIsNotNone(BaseModel.__doc__)
        self.assertIsNotNone(BaseModel.__init__.__doc__)
        self.assertIsNotNone(BaseModel.__str__.__doc__)
        self.assertIsNotNone(BaseModel.save.__doc__)
        self.assertIsNotNone(BaseModel.to_dict.__doc__)

    def test_class_has_docstring(self):
        self.assertIsNotNone(BaseModel.__doc__)

    def test_str_return_value(self):
        expected_output = f"[BaseModel] ({self.base_model_1.id}) {self.base_model_1.__dict__}"
        self.assertEqual(str(self.base_model_1), expected_output)

    def test_unique_ids(self):
        self.assertNotEqual(self.base_model_1.id, self.base_model_2.id)

    def test_updated_at_updated(self):
        initial_time = self.base_model_1.updated_at
        self.base_model_1.save()
        self.assertNotEqual(initial_time, self.base_model_1.updated_at)

    def test_to_dict_iso_format(self):
        model_dict = self.base_model_1.to_dict()
        self.assertEqual(model_dict['__class__'], 'BaseModel')
        self.assertIsInstance(model_dict['updated_at'], str)
        self.assertIsInstance(model_dict['created_at'], str)

    def test_attribute_data_types(self):
        self.assertIsInstance(self.base_model_1.updated_at, datetime)
        self.assertIsInstance(self.base_model_1.created_at, datetime)
        self.assertIsInstance(self.base_model_1.id, str)

    def test_different_uuids(self):
        self.assertNotEqual(self.base_model_1.id, self.base_model_2.id)

    def test_nonexistent_attribute_method(self):
        with self.assertRaises(AttributeError):
            getattr(self.base_model_1, 'nonexistent_attr')
        with self.assertRaises(AttributeError):
            getattr(self.base_model_1, 'nonexistent_method')()

    def test_created_updated_same_time(self):
        self.assertEqual(self.base_model_1.created_at, self.base_model_1.updated_at)

    def test_instantiation_from_dict(self):
        model_dict = self.base_model_1.to_dict()
        new_model = BaseModel(**model_dict)
        self.assertEqual(new_model.to_dict(), model_dict)

    def test_class_name_in_to_dict(self):
        model_dict = self.base_model_1.to_dict()
        self.assertIn('__class__', model_dict)
        self.assertEqual(model_dict['__class__'], 'BaseModel')

    def test_type_error_to_dict(self):
        with self.assertRaises(TypeError):
            self.base_model_1.to_dict(123)

    def test_same_uuid_datetime_from_dict(self):
        model_dict = self.base_model_1.to_dict()
        new_model = BaseModel(**model_dict)
        self.assertEqual(new_model.id, self.base_model_1.id)
        self.assertEqual(new_model.created_at, self.base_model_1.created_at)

    def test_invalid_date_instantiation_from_dict(self):
        model_dict = self.base_model_1.to_dict()
        model_dict['created_at'] = 'invalid_date_format'
        with self.assertRaises(ValueError):
            BaseModel(**model_dict)

    def test_updated_created_data_types_from_dict(self):
        model_dict = self.base_model_1.to_dict()
        new_model = BaseModel(**model_dict)
        self.assertIsInstance(new_model.updated_at, datetime)
        self.assertIsInstance(new_model.created_at, datetime)

    def test_iso_dates_in_dict(self):
        model_dict = self.base_model_1.to_dict()
        self.assertTrue(isinstance(model_dict['updated_at'], str) and isinstance(model_dict['created_at'], str))

    def test_to_dict_returns_dict(self):
        self.assertIsInstance(self.base_model_1.to_dict(), dict)

    def test_type_error_save(self):
        with self.assertRaises(TypeError):
            self.base_model_1.save(123)

    def test_json_file_created_on_save(self):
        self.assertFalse(os.path.exists("file.json"))
        self.base_model_1.save()
        self.assertTrue(os.path.exists("file.json"))

    def test_storage_instance_type(self):
        self.base_model_1.save()
        with open("file.json", 'r') as file:
            data = json.load(file)
            for key in data.keys():
                self.assertIsInstance(data[key], dict)

    def test_updated_at_updated_on_save(self):
        initial_time = self.base_model_1.updated_at
        self.base_model_1.save()
        self.assertNotEqual(initial_time, self.base_model_1.updated_at)


if __name__ == '__main__':
    unittest.main()
