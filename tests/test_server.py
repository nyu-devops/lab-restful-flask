# Copyright 2016, 2017 John J. Rofrano. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Test cases for the Pet Service

Test cases can be run with:
  nosetests
  coverage report -m
"""

import logging
import unittest
import json
from flask_api import status    # HTTP Status Codes
import app.routes as service

######################################################################
#  T E S T   C A S E S
######################################################################
class TestPetServer(unittest.TestCase):
    """ Pet Server Tests """

    @classmethod
    def setUpClass(cls):
        """ Run once before all tests """
        service.app.debug = False
        service.initialize_logging(logging.ERROR)

    def setUp(self):
        """ Runs before each test """
        service.Pet.remove_all()
        service.Pet(0, 'fido', 'dog').save()
        service.Pet(0, 'kitty', 'cat').save()
        self.app = service.app.test_client()

    def tearDown(self):
        """ Runs after each test """
        service.Pet.remove_all()

    def test_index(self):
        """ Test the Home Page """
        resp = self.app.get('/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = json.loads(resp.data)
        self.assertEqual(data['name'], 'Pet Demo REST API Service')

    def test_get_pet_list(self):
        """ Get a list of Pets """
        resp = self.app.get('/pets')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = json.loads(resp.data)
        self.assertEqual(len(data), 2)

    def test_get_pet(self):
        """ Get one Pet """
        resp = self.app.get('/pets/2')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = json.loads(resp.data)
        self.assertEqual(data['name'], 'kitty')

    def test_get_pet_not_found(self):
        """ Get a Pet thats not found """
        resp = self.app.get('/pets/0')
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_pet(self):
        """ Create a Pet """
        # save the current number of pets for later comparrison
        pet_count = self.get_pet_count()
        # add a new pet
        new_pet = {'name': 'sammy', 'category': 'snake'}
        data = json.dumps(new_pet)
        resp = self.app.post('/pets', data=data, content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        # Make sure location header is set
        location = resp.headers.get('Location', None)
        self.assertIsNotNone(location)
        # Check the data is correct
        new_json = json.loads(resp.data)
        self.assertEqual(new_json['name'], 'sammy')
        # check that count has gone up and includes sammy
        resp = self.app.get('/pets')
        data = json.loads(resp.data)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(data), pet_count + 1)
        self.assertIn(new_json, data)

    def test_spoof_pet_id(self):
        """ Create a Pet passing in an id """
        # add a new pet
        new_pet = {'id': 999, 'name': 'sammy', 'category': 'snake'}
        data = json.dumps(new_pet)
        resp = self.app.post('/pets', data=data, content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        # Make sure location header is set
        location = resp.headers.get('Location', None)
        self.assertIsNotNone(location)
        # Check the data is correct
        new_json = json.loads(resp.data)
        self.assertEqual(new_json['name'], 'sammy')
        self.assertNotEqual(new_json['id'], 999)

    def test_update_pet(self):
        """ Update a Pet """
        new_kitty = {'name': 'kitty', 'category': 'tabby'}
        data = json.dumps(new_kitty)
        resp = self.app.put('/pets/2', data=data, content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        resp = self.app.get('/pets/2', content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        new_json = json.loads(resp.data)
        self.assertEqual(new_json['category'], 'tabby')

    def test_update_pet_with_no_name(self):
        """ Update a Pet with no name """
        new_pet = {'category': 'dog'}
        data = json.dumps(new_pet)
        resp = self.app.put('/pets/2', data=data, content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_pet_not_found(self):
        """ Update a Pet that can't be found """
        new_kitty = {"name": "timothy", "category": "mouse"}
        data = json.dumps(new_kitty)
        resp = self.app.put('/pets/0', data=data, content_type='application/json')
        self.assertEquals(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_pet(self):
        """ Delete a Pet that exists """
        # save the current number of pets for later comparrison
        pet_count = self.get_pet_count()
        # delete a pet
        resp = self.app.delete('/pets/2', content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(len(resp.data), 0)
        new_count = self.get_pet_count()
        self.assertEqual(new_count, pet_count - 1)

    def test_create_pet_with_no_name(self):
        """ Create a Pet with the name missing """
        new_pet = {'category': 'dog'}
        data = json.dumps(new_pet)
        resp = self.app.post('/pets', data=data, content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_nonexisting_pet(self):
        """ Get a Pet that doesn't exist """
        resp = self.app.get('/pets/5')
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_query_pet_list_by_category(self):
        """ Query Pets by Category """
        resp = self.app.get('/pets', query_string='category=dog')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertTrue(len(resp.data) > 0)
        self.assertTrue('fido' in resp.data)
        self.assertFalse('kitty' in resp.data)
        data = json.loads(resp.data)
        query_item = data[0]
        self.assertEqual(query_item['category'], 'dog')

    def test_method_not_allowed(self):
        """ Call a Method thats not Allowed """
        resp = self.app.post('/pets/0')
        self.assertEqual(resp.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


######################################################################
# Utility functions
######################################################################

    def get_pet_count(self):
        """ save the current number of pets """
        resp = self.app.get('/pets')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = json.loads(resp.data)
        return len(data)


######################################################################
#   M A I N
######################################################################
if __name__ == '__main__':
    unittest.main()
