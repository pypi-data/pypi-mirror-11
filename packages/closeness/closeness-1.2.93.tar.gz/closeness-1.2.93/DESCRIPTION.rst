Mongodb relation finder 
=======================

This is project is using to find relationship between mongodb documents

This will be the initial version of the project


How to use:

Install package with pip


.. code-block:: console

   pip install closeness


See the example,

.. code-block::

   from closeness.closeness_aggregation import ClosenessAggregation
   from pymongo import MongoClient
   client = MongoClient()
   db = client.test_database
   user_collection = db.user_collection
