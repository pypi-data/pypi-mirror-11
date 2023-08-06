Flask-CassandraDB
=================

.. image:: https://pypip.in/v/Flask-CassandraDB/badge.png
    :target: https://pypi.python.org/pypi/Flask-CassandraDB
    :alt: Latest PyPI version

.. image:: https://travis-ci.org/youngking/flask-cassandradb.png
   :target: https://travis-ci.org/youngking/flask-cassandradb
   :alt: Latest Travis CI build status

connect cassandra to flask

Usage
-----

This is an example flask app that reads from a Cassandra cluster::


    from flask import Flask
    from flask_cassandradb import CassandraCluster

    app = Flask(__name__)
    cassandra = CassandraCluster()

    app.config['CASSANDRA_NODES'] = ['cassandra01.flyzen.com']  # can be a string or list of nodes
    app.config['CASSANDRA_KEYSPACE'] = 'pythonista' # default keyspace


    @app.route("/cassandra_test")
    def cassandra_test():
        session = cassandra.connect("monty_python") # connect to the monty_python keyspace, it not specified will use the default keyspace.
        cql = "SELECT * FROM sketches LIMIT 1"
        r = session.execute(cql)
        return str(r[0])

    if __name__ == '__main__':
        app.run()


Installation
------------
::

    $ pip install flask-cassandradb

Requirements
^^^^^^^^^^^^

Compatibility
-------------

Licence
-------

Authors
-------

`Flask-CassandraDB` was written by `Young King <yanckin@gmail.com>`_.
