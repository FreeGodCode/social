import os

from flask_script import Manager

from app import create_app

# from flask import Flask
#
# app = Flask(__name__)
config_name = os.environ.get('FLASK_CONFIG') or 'development'
app = create_app(config_name)

manager = Manager(app)

# @app.route('/')
# def hello_world():
#     return 'Hello World!'


if __name__ == '__main__':
    # app.run()
    manager.run()
