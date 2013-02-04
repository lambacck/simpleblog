import os

from simpleblog.wsgi import application as _application


def application(environ, start_response):
    os.environ['SECRET_KEY'] = environ['SECRET_KEY']
    os.environ['SIMPLEBLOG_DB_PASSWORD'] = environ['SIMPLEBLOG_DB_PASSWORD']
    return _application(environ, start_response)
