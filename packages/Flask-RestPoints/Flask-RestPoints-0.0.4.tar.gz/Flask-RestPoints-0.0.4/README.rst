Flask-RestPoints
================

`Flask-RestPoints`_ is an extension to `Flask`_ that allows adds a few
health check endpoints (ping, epoch, and status) to the Flask application.

::

    from flask import Flask
    from flask_restpoints import RestPoints

    app = Flask(__name__)
    rest = RestPoints(app)

    @rest.status_job(name="PostgreSQL", timeout=5)
    def postgresql():
        # Perform a ping/query to Postgres

    @rest.status_job
    def facebook
        # Ping some Facebook service.


get Flask_RestPoints
====================

Install `flask`_

    sudo easy_install Flask-RestPoints

Download the latest release from `Python Package Index`_
or clone `the repository`_

.. _Flask-Genshi: http://packages.python.org/Flask-RestPoints
.. _Flask: http://flask.pocoo.org/
.. _the repository: https://github.com/juztin/flask-restpoints
.. _Python Package Index: https://pypi.python.org/pypi/Flask-RestPoints
