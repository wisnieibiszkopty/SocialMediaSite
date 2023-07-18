import os
from flask import Flask
from . import base, profile


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(SECRET_KEY='dev')

    app.config['dbconfig'] = {'host': '127.0.0.1',
                              'user': 'website_admin',
                              'password': 'website',
                              'database': 'social_media'}

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    app.register_blueprint(base.bp)
    app.register_blueprint(profile.bp)

    return app
