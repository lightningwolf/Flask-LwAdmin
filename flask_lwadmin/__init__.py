#!/usr/bin/env python
# coding=utf8

from flask import Blueprint


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


class Navbar:
    NO_URL = 0
    URL_INTERNAL = 1
    URL_EXTERNAL = 2
    DIVIDER = 3

    _navbar = {'brand': 'Project Name', 'username': None, 'items': [], 'profile_items': []}
    _items = {}

    def set_brand(self, brand):
        self._navbar['brand'] = brand

    def set_username(self, username):
        self._navbar['username'] = username

    def add_item(self, key, label, url=None, type=None, controller=None, disabled=False):
        item = self.__create_base_item(label, url, type, controller, disabled)
        item['menus'] = []
        self._items[key] = item
        self._navbar['items'].append(key)

    def add_sub_item(self, parent_key, key, label, url=None, type=None, controller=None, disabled=False):
        item = self.__create_base_item(label, url, type, controller, disabled)
        self._items[key] = item
        self._items[parent_key]['menus'].append(key)

    def add_profile_item(self, key, label, url=None, type=None, controller=None, disabled=False):
        item = self.__create_base_item(label, url, type, controller, disabled)
        self._items[key] = item
        self._navbar['profile_items'].append(key)

    def get_item(self, key):
        return self._items[key]

    def get_navbar(self):
        return self._navbar

    def __create_base_item(self, label, url=None, type=None, controller=None, disabled=False):
        if type is None:
            type = self.NO_URL

        item = {'label': label, 'type': type, 'url': url, 'disabled': disabled}
        if controller is not None:
            item['controller'] = controller

        return item
