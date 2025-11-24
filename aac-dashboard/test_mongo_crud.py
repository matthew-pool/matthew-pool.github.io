"""
Methods: setUp(), tearDown(), @classmethod: setUpClass() & tearDownClass(), test_*

unittest.TestCase Assert Methods (optional arg: msg="error message"):
    assertEqual, assertNotEqual, assertTrue, assertFalse,
    assertIs, assertIsNot, assertIsNone, assertIsNotNone, assertIn, assertNotIn,
    assertIsInstance, assertNotIsInstance, assertRaises(exception, *, msg=None)
"""
from mongo_crud import MongoCrud
import unittest

# TODO: create tests for checking network and database connection


class TestMongoCrud(unittest.TestCase):
    """ Class to test MongoCrud class in mongo_crud.py module """

    def setUp(self):  # Runs before each test
        self.id = {'_id': '01234567'}
        self.some_query = {'key': 'value'}
        self.some_dict = {'key': 'value'}
        self.some_list = ['list item1', 'list item2']
        self.empty_query = {}
        self.empty_dict = {}
        self.empty_animal = {}
        self.custom_animal = {
            'age_upon_outcome': '2 years',
            'animal_type': 'Dog',
            'breed': 'Dachshund',
            'color': 'Blue',
            'date_of_birth': '2022-09-13'
        }

        self.mongo_crud = MongoCrud()  # Creates a fresh new instance before each test
        self.mongo_crud.database.collection.delete_many(self.id)

    def tearDown(self):  # Runs after each test
        self.mongo_crud.database.collection.delete_many(self.custom_animal)
        self.mongo_crud.database.collection.delete_many(self.id)

    # NOTE: initial instance attribute values should be tested here


    def test_create_empty(self):
        with self.assertRaises(ValueError):
            self.mongo_crud.create(self.empty_animal)

    def test_create_wrong_type(self):
        with self.assertRaises(ValueError):
            corrupt_animal = self.some_list  # instead of {...}
            self.mongo_crud.create(corrupt_animal)

    def test_create_success(self):
        result = self.mongo_crud.create(self.custom_animal)
        self.assertEqual(result, True)

    """ NOTE: placeholder test function in case original function modified to 'raise'
    def test_create_duplicate(self):
        with self.assertRaises(DuplicateKeyError):
            self.mongo_crud.create(self.id)
            result = self.mongo_crud.create(self.id)  # failure due to DuplicateKeyError
            # self.assertFalse(result)
    """


    def test_read_empty(self):
        with self.assertRaises(ValueError):
            self.mongo_crud.read(self.empty_query)

    def test_read_wrong_type(self):
        with self.assertRaises(ValueError):
            query_filter = self.some_list  # instead of correct {...}
            self.mongo_crud.read(query_filter)

    def test_read_success(self):
        some_breed = 'Maltese Mix'
        result = self.mongo_crud.read({'breed': some_breed})
        self.assertTrue(result)

    def test_read_nonexistent(self):
        nonexistent_breed = 'silly lil wiener dog breed'
        result = self.mongo_crud.read({'breed': nonexistent_breed})
        self.assertFalse(result)


    def test_update_empty_query(self):
        with self.assertRaises(ValueError):
            self.mongo_crud.update(self.empty_query, self.some_dict)

    def test_update_empty_dict(self):
        with self.assertRaises(ValueError):
            self.mongo_crud.update(self.some_query, self.empty_dict)

    def test_update_wrong_type_query(self):
        with self.assertRaises(ValueError):
            corrupt_query = self.some_list
            self.mongo_crud.update(corrupt_query, self.some_dict)

    def test_update_wrong_type_dict(self):
        with self.assertRaises(ValueError):
            corrupt_dict = self.some_list
            self.mongo_crud.update(self.some_query, corrupt_dict)

    def test_update_success(self):
        self.mongo_crud.create(self.custom_animal)
        custom_query = self.custom_animal
        result = self.mongo_crud.update(custom_query, self.some_dict)
        self.assertGreater(result, 0)  # Indicates at least one document updated

    def test_update_nonexistent_id(self):
        result = self.mongo_crud.update(self.id, self.some_dict)
        self.assertEqual(result, 0)  # Indicates 0 documents updated


    def test_delete_empty(self):
        with self.assertRaises(ValueError):
            self.mongo_crud.delete(self.empty_dict)

    def test_delete_wrong_type(self):
        with self.assertRaises(ValueError):
            corrupt_query = self.some_list
            self.mongo_crud.delete(corrupt_query)

    def test_delete_success(self):
        self.mongo_crud.create(self.id)
        result = self.mongo_crud.delete(self.id)
        self.assertGreater(result, 0)  # Indicates at least one document deleted


if __name__ == "__main__":
    print('Executing main script...\n')
    unittest.main(argv=['first-arg-ignored'], exit=False)  # Allows for test console output
    print('Finished!')
