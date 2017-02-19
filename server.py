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

import os
import logging
from threading import Lock
from flask import Flask, Response, jsonify, request, make_response, json

# Create Flask application
app = Flask(__name__)

# Status Codes
HTTP_200_OK = 200
HTTP_201_CREATED = 201
HTTP_204_NO_CONTENT = 204
HTTP_400_BAD_REQUEST = 400
HTTP_404_NOT_FOUND = 404
HTTP_409_CONFLICT = 409

# Lock for thread-safe counter increment
lock = Lock()

# dummy data for testing
current_pet_id = 2
pets = [
    {
        'id': 1,
        'name': 'fido',
        'kind': 'dog'
    },
    {
        'id': 2,
        'name': 'kitty',
        'kind': 'cat'
    }
]

######################################################################
# GET INDEX
######################################################################
@app.route('/')
def index():
    pets_url = request.base_url + "pets"
    return make_response(jsonify(name='Pet Demo REST API Service',
                   version='1.0',
                   url=pets_url
                   ), HTTP_200_OK)

######################################################################
# LIST ALL PETS
######################################################################
@app.route('/pets', methods=['GET'])
def list_pets():
    results = []
    kind = request.args.get('kind')
    if kind:
        results = [pet for pet in pets if pet['kind'] == kind]
    else:
        results = pets

    return make_response(jsonify(results), HTTP_200_OK)

######################################################################
# RETRIEVE A PET
######################################################################
@app.route('/pets/<int:id>', methods=['GET'])
def get_pets(id):
    index = [i for i, pet in enumerate(pets) if pet['id'] == id]
    if len(index) > 0:
        message = pets[index[0]]
        rc = HTTP_200_OK
    else:
        message = { 'error' : 'Pet with id: %s was not found' % str(id) }
        rc = HTTP_404_NOT_FOUND

    return make_response(jsonify(message), rc)

######################################################################
# ADD A NEW PET
######################################################################
@app.route('/pets', methods=['POST'])
def create_pets():
    payload = request.get_json()
    if is_valid(payload):
        id = next_index()
        pet = {'id': id, 'name': payload['name'], 'kind': payload['kind']}
        pets.append(pet)
        message = pet
        rc = HTTP_201_CREATED
    else:
        message = { 'error' : 'Data is not valid' }
        rc = HTTP_400_BAD_REQUEST

    return make_response(jsonify(message), rc)

######################################################################
# UPDATE AN EXISTING PET
######################################################################
@app.route('/pets/<int:id>', methods=['PUT'])
def update_pets(id):
    index = [i for i, pet in enumerate(pets) if pet['id'] == id]
    if len(index) > 0:
        payload = request.get_json()
        if is_valid(payload):
            pets[index[0]] = {'id': id, 'name': payload['name'], 'kind': payload['kind']}
            message = pets[index[0]]
            rc = HTTP_200_OK
        else:
            message = { 'error' : 'Pet data was not valid' }
            rc = HTTP_400_BAD_REQUEST
    else:
        message = { 'error' : 'Pet %s was not found' % id }
        rc = HTTP_404_NOT_FOUND

    return make_response(jsonify(message), rc)

######################################################################
# DELETE A PET
######################################################################
@app.route('/pets/<int:id>', methods=['DELETE'])
def delete_pets(id):
    index = [i for i, pet in enumerate(pets) if pet['id'] == id]
    if len(index) > 0:
        del pets[index[0]]
    return make_response('', HTTP_204_NO_CONTENT)

######################################################################
#  U T I L I T Y   F U N C T I O N S
######################################################################
def next_index():
    global current_pet_id
    with lock:
        current_pet_id += 1
    return current_pet_id

def is_valid(data):
    valid = False
    try:
        name = data['name']
        kind = data['kind']
        valid = True
    except KeyError as err:
        app.logger.warn('Missing parameter error: %s', err)
    except TypeError:
        app.logger.warn('Invalid Content Type error')

    return valid

# @app.before_first_request
# def setup_logging():
#     if not app.debug:
#         # In production mode, add log handler to sys.stderr.
#         app.logger.addHandler(logging.StreamHandler())
#         app.logger.setLevel(logging.INFO)


######################################################################
#   M A I N
######################################################################
if __name__ == "__main__":
    # Pull options from environment
    debug = (os.getenv('DEBUG', 'False') == 'True')
    port = os.getenv('PORT', '5000')
    app.run(host='0.0.0.0', port=int(port), debug=debug)
