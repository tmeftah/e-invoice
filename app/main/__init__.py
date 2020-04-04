import sys
from os.path import abspath, dirname, join, pardir
from importlib import import_module
from flask import Flask, current_app
from flask_cors import CORS
from app.main.resources import db, api, jwt
from app.main.config import config_by_name


# prevent python from writing *.pyc files / __pycache__ folders
sys.dont_write_bytecode = True

# path_source = dirname(abspath(__file__))
# path_parent = abspath(join(path_source, pardir))
# if path_source not in sys.path:
#     sys.path.append(path_source)


list_of_module = ['auth', 'users', 'products']


def register_modules(modules_list):
    for module_name in modules_list:
        module = import_module(__name__+'.{}'.format(module_name))


def register_extension(app):
    db.init_app(app)
    api.init_app(app)
    jwt.init_app(app)


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])
    CORS(app)
    register_modules(list_of_module)
    register_extension(app)

    @app.before_first_request
    def create_tables():
        db.create_all()
    return app


if __name__ == '__main__':
    app = create_app('dev')
    app.run()
