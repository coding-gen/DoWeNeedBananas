# Copyright 2016 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from .Model import Model
from google.cloud import datastore
from datetime import datetime
import sys


def groceries_formatter(entity):
    """
    Translates Datastore results into the format expected by the
    application.

    Datastore typically returns:
        [Entity{key: (kind, id), prop: val, ...}]

    This returns:
        [ id, org, description, address, phone, hours, review, created_on ]
    where each entity is a Python string
    except id which is an int, 
    and created_on which is a Python datetime
    """
    if not entity:
        return None
    if isinstance(entity, list):
        entity = entity.pop()
    return [\
        entity['product'], \
        entity['category'], \
        entity['location'], \
        entity['description'], \
        entity['image'] \
        ]


class model(Model):
    def __init__(self):
        """
        Initialize the Datastore client in the desired project.
        Be sure to set the GOOGLE_APPLICATION_CREDENTIALS environment variable so you have access.
        We track an id in the grocery, but it is keyed on the kind and product name.
        This is because you don't want duplicates in a grocery list, 
        so entering the same product name again merely overwrites.

        :raises: Database errors on connection and deletion
        """
        self.client = datastore.Client('cloud-lalonde-sgl')
        query = self.client.query(kind = 'Groceries')
        groceriesDump = list(map(groceries_formatter,query.fetch()))
        self.grocID = len(groceriesDump) + 1

    def select(self):
        query = self.client.query(kind = 'Groceries')
        groceriesDump = list(map(groceries_formatter,query.fetch()))
        return groceriesDump

    def filtered_select(self, key, value):
        query = self.client.query(kind = 'Groceries')
        query.add_filter(key, '=', value)
        groceriesDump = list(map(groceries_formatter,query.fetch()))
        return groceriesDump


    def insert(self, product, category, location, description, image):
        """
        Add a new grocery item to Datastore in the Groceries kind
        :param product: String
        :param category: String
        :param location: String
        :param description: String
        :param image: String
        :return: True
        :raises: Database errors on connection and deletion
        """

        key = self.client.key('Groceries', product)
        groc = datastore.Entity(key)
        groc.update( {
            'id': self.grocID,
            'product': product, 
            'category': category,
            'location': location,
            'description': description,
            'image': image
            })
        self.client.put(groc)
        self.grocID += 1
        return True


    def delete(self, product):
        """
        Deletes entry from kind in Datastore if it exists
        :param product: String
        :return: True
        :raises: Database errors on connection and deletion
        """
        key = self.client.key('Groceries', product)
        groc = datastore.Entity(key)
        self.client.delete(key)
        return True


    def update(self, product, category):
        """
        TODO implement

        Updates product and/or category
        :param product: String
        :param category: String
        :return: True
        :raises: Database errors on connection and deletion
        """
        pass