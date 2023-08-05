Planningalerts Data Library
===========================

.. image:: https://drone.io/bitbucket.org/otherchirps/morph_planningalerts/status.png
  :target: https://drone.io/bitbucket.org/otherchirps/morph_planningalerts/latest

Aims to provide a simple, standardised perisistance layer for `PlanningAlerts <https://www.planningalerts.org.au>`_ records.

Mainly intended to use when writing PlanningAlerts scrapers on `morph.io <https://morph.io>`_.  Morph python environments already 
have nice libraries, like `scraperwiki <https://github.com/openaustralia/scraperwiki-python/tree/morph_defaults>`_ installed, but those don't enforce the data `requirements <https://www.planningalerts.org.au/how_to_write_a_scraper>`_ 
expected by PlanningAlerts. This library attempts to do so.


Installation
------------

From source
~~~~~~~~~~~

``python setup.py install``

pip
~~~

``pip install morph_planningalerts``

Usage
-----

.. code-block:: python

   from morph_planningalerts import DevelopmentApplication, MorphDatabase

   # Make sure the database file exists. If it does, this won't do anything.
   MorphDatabase.init()
   
   # Time passes... data is scraped...
   new_record = DevelopmentApplication.create(
       council_reference='M123/456',
       address='64 Zoo Lane',
       description='this is the least info needed to prevent explosions',
       info_url='http://detail_page_about_application',
       comment_url='http://some_feedback_url'
   )

   # Or, if you only want to insert new records:
   record, was_created = DevelopmentApplication.create_or_get(
       council_reference=...
   )

For more examples, check out the docs on `querying with the Peewee ORM <http://peewee.readthedocs.org/en/latest/peewee/querying.html>`_.

Source code
-----------

You can get the code here:

https://bitbucket.org/otherchirps/morph_planningalerts


Testing
-------
 
`tox <https://pypi.python.org/pypi/tox>`_ is being used to run the tests across
python 2.7 & 3.x. 

To bootstrap your test environment, the easiest way is you 
use the `pip <https://pip.pypa.io/en/latest/installing.htm>`_ requirements file::

    pip install -r requirements.txt

Then you can simply run::

    tox


