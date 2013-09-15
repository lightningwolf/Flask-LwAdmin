#!/usr/bin/env python
# coding=utf8
from flask import Blueprint


class ConfigurationError(RuntimeError):
    pass


class LwAdmin(object):

    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        blueprint = Blueprint(
            'lwadmin',
            __name__,
            template_folder='templates',
            static_folder='static',
            static_url_path=app.static_url_path + '/lwadmin')

        app.register_blueprint(blueprint)
