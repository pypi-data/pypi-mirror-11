MongoSessionFactory
===================
Translation and bug fix in progress.

MongoDB-based session factory. You can try https://pypi.python.org/pypi/mongodb-beaker2 which released in 2012... I couldn't, I gave up.

To be honest, it is a modified version of ``pyramid.session.BaseCookieSessionFactory`` with the same behavior.

Installation
------------

Install the extension with::

    $ pip install pyramid_mongo_session

or::

    $ easy_install pyramid_mongo_session


Dependencies
------------

MongoDB team have decided to change an API. Now here is ``update_one`` and ``replace_one`` instead of cute ``update`` etc.
I don't want to see "You are still using a deprecated function!", and... you know... you don't want this too. Yep. MongoDB 3.x! Pymongo 3.0.3! Cutting edge of progress.


Usage
-----

.. code-block:: python

    MongoSessionFactory(
        collection,
        to_pickle=False,
        cookie_name='session',
        max_age=None,
        path='/',
        domain=None,
        secure=False,
        httponly=False,
        timeout=3600,
        reissue_time=0,
        set_on_exception=True,
    )

``collection`` means ``pymongo.MongoClient collection``. Not the string but collection itself. ``to_pickle`` is chosen to be False.

Yep, fully synchronous way. Do you believe in async pyramid? I don't. ``MongoSessionFactory`` is using common db-connection.

Default values are very useful, I swear (again). Session lifetime is one hour (by default).


.. code-block:: python

    # encoding: utf-8

    from pyramid.config import Configurator
    from pyramid_mongo_session import MongoSessionFactory
    ...

    def main(global_config, **settings):
        """ This function returns a Pyramid WSGI application.
        """        
        config = Configurator(settings=settings)

        session_factory = MongoSessionFactory(
            collection=MongoClient('localhost', 27017).your_db.session)
        config.set_session_factory(session_factory)
        ...
        return config.make_wsgi_app()


Schema
------

Current schema in schemaless MongoDB is:

::

    {
        '_id': session identifier,
        'created': float value of creation time
        'accessed': float value of accessed time,
        'value': value of the session object itself,
        'pickled': value pickled?
    }

You can sometimes cleanup the database by removing too old documents... I think. But indexes is your business. _id have primary index by default, it is fast as hell.


Important notes
---------------

``to_pickle`` DISABLED BY DEFAULT. That means you can store in session only primitive types of the objects: strings, lists, numbers (int and float), dictionaries with primitive types and with string keys etc.
Flashing messages, data like {'user': 'admin', 'password': 'love'} etc. And you save some CPU time!

If you want to store something more implicitly like python methods or SQLA objects, you need to change this to True. You can change it at any time and documents will be replaced one by one when accessed.


Mass Logout
-----------

::

    db.session.remove({})


Muahahahahah.


Testing
-------

::

    $ python setup.py test


It is using default existing ``test`` database with collection ``session``.

Any help to proving this readme file (and package) would be highly appreciated.
