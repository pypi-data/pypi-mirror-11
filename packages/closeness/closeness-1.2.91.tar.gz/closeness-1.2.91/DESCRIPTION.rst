Mongodb relation finder 
=======================

This is project is using to find relationship between mongodb documents

This will be the initial version of the project


How to use:

Install package with pip


.. code-block:: console

   pip install closeness


See the example,

.. code-block:: python
   :linenos:

   from closeness.closeness_aggregation import ClosenessAggregation
   from pymongo import MongoClient
   client = MongoClient()
   db = client.test_database
   user_collection = db.user_collection
   user1 = {
      'name': 'User 1',
      'age': 25,
      'gender': 'male',
      'tags': [
         "tag1",
         "tag2",
         "tag3",
      ],
      'friends': [
         {"user_id": "friend1", 'name': "name1"},
         {"user_id": "friend2", 'name': "name2"},
         {"user_id": "friend3", 'name': "name3"},
      ]
   }
   user2 = {
      'name': 'User 2',
      'age': 25,
      'gender': 'male',
      'tags': [
         "tag1",
         "tag2",
         "tag3",
      ],
      'friends': [
         {"user_id": "friend1", 'name': "name1"},
         {"user_id": "friend2", 'name': "name2"},
         {"user_id": "friend3", 'name': "name3"},
      ]
   }
   user3 = {
      'name': 'User 3',
      'age': 30,
      'gender': 'female',
      'tags': [
         "tag1",
      ],
      'friends': [
         {"user_id": "friend3", 'name': "name3"},
      ]
   }
