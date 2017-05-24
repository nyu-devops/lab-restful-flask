# Copyright 2016 John Rofrano. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from flask import url_for

class DataValidationError(Exception):
    pass

class Pet(object):
    __data = []
    __index = 0

    def __init__(self, id=0, name=None, category=None):
        self.id = id
        self.name = name
        self.category = category

    def save(self):
        if self.id == 0:
            self.id = self.__next_index()
            Pet.__data.append(self)
        else:
            for i in range(len(Pet.__data)):
                if Pet.__data[i].id == self.id:
                    Pet.__data[i] = self
                    break

    def delete(self):
        Pet.__data.remove(self)

    def __next_index(self):
        Pet.__index += 1
        return Pet.__index

    def serialize(self):
        return { "id": self.id, "name": self.name, "category": self.category }

    def self_url(self):
        return url_for('get_pets', id=self.id, _external=True)

    def deserialize(self, data):
        if not isinstance(data, dict):
            raise DataValidationError('Invalid pet: body of request contained bad or no data')
        id = 0
        if data.has_key('id'):
            self.id = data['id']
        try:
            self.name = data['name']
            self.category = data['category']
        except KeyError as e:
            raise DataValidationError('Invalid pet: missing ' + e.args[0])

    @staticmethod
    def all():
        return [pet for pet in Pet.__data]

    @staticmethod
    def remove_all():
        del Pet.__data[:]
        Pet.__index = 0
        return Pet.__data

    @staticmethod
    def find(id):
        if len(Pet.__data) == 0:
            return None
        pets = [pet for pet in Pet.__data if pet.id == id]
        if len(pets) > 0:
            return pets[0]
        return None

    @staticmethod
    def find_by_category(category):
        return [pet for pet in Pet.__data if pet.category == category]
