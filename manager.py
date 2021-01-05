import os

from flask_script import Manager

from app import create_app

config_name = os.environ.get('FLASK_CONFIG') or 'development'
app = create_app(config_name)

manager = Manager(app)

if __name__ == '__main__':
    # app.run()
    manager.run()
