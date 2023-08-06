Flask-Tracy
=============

`Flask-Tracy`_ is an extension to `Flask`_ that logs tracing information
per request.  

Time, url, client IP, client name, transaction ID, and 
request duration are logged as informational.

`TRACY_REQURE_CLIENT` (OPTIONAL) configuration boolean used to return a 
400 when no client name header (defaults to `Trace-ID`) is present.

::

    from flask import Flask
    from flask.ext.tracy import Tracy

    app = Flask(__name__)
    appp.config.from_object('some_file.ini')
    Tracy(app)


    @app.route('/')
    def index()
        return "Hello World"


get Flask-Tracy
====================

Install `flask`_

    pip install Flask-Tracy

Download the latest release from `Python Package Index`_
or clone `the repository`_

.. _Flask: http://flask.pocoo.org/
.. _the repository: https://github.com/juztin/flask-tracy


