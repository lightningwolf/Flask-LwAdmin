#!/usr/bin/env python
# coding=utf8

from flask import Blueprint, url_for


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

    _navbar = {'brand': 'Project Name', 'user': None, 'items': [], 'profile_items': []}
    _items = {}

    def set_brand(self, brand):
        self._navbar['brand'] = brand

    def set_username(self, username, url=None, type=None, controller=None, disabled=False):
        item = self.__create_base_item(username, url, type, controller, disabled)
        self._navbar['user'] = item

    def add_item(self, key, label, url=None, type=None, controller=None, disabled=False):
        self.__check_key(key)
        item = self.__create_base_item(label, url, type, controller, disabled)
        item['menus'] = []
        self._items[key] = item
        self._navbar['items'].append(key)

    def add_sub_item(self, parent_key, key, label, url=None, type=None, controller=None, disabled=False):
        self.__check_key(key)
        item = self.__create_base_item(label, url, type, controller, disabled)
        item['parent'] = parent_key
        self._items[key] = item
        self._items[parent_key]['menus'].append(key)

    def add_profile_item(self, key, label, url=None, type=None, controller=None, disabled=False):
        self.__check_key(key)
        item = self.__create_base_item(label, url, type, controller, disabled)
        self._items[key] = item
        self._navbar['profile_items'].append(key)

    def get_item(self, key):
        if key not in self._items:
            RuntimeError('This key: %s not exists' % key)
        return self._items[key]

    def get_data(self):
        return self._navbar

    def get_brand(self):
        return self._navbar['brand']

    def get_user(self):
        return self._navbar['user']

    def get_menu(self):
        menu = []
        for key in self._navbar['items']:
            item = self.get_item(key)
            if item['type'] == self.URL_INTERNAL:
                item['url'] = url_for(item['url'])
            menu.append(item)
        return menu

    def __create_base_item(self, label, url=None, type=None, controller=None, disabled=False):
        if type is None:
            type = self.NO_URL

        if type == self.NO_URL:
            url = '#'

        item = {'label': label, 'type': type, 'url': url, 'disabled': disabled, 'active': False}
        if controller is not None:
            item['controller'] = controller

        return item

    def __check_key(self, key):
        if key in self._items:
            RuntimeError('This key: %s is not unique' % key)
        return True
