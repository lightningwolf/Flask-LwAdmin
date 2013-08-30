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

def create_navbar_fd(conf={}):
    """Creating navbar from dictionary type configuration"""
    navbar = Navbar()
    brand = conf.get('brand', {})
    navbar.set_brand(
        brand_name=brand.get('brand_name', None),
        brand_url=brand.get('brand_url', None),
        brand_html=brand.get('brand_html', None)
    )
    items = conf.get('items', [])
    for item in items:
        if 'key' not in item.keys():
            RuntimeError('Menu items must have unique key')

        if 'label' not in item.keys():
            RuntimeError('Menu items must have label')

        navbar.add_menu_item(
            item['key'],
            item['label'],
            item.get('url', None),
            item.get('type', None),
            item.get('controller', None),
            item.get('disabled', False)
        )

        if 'icon' in item.keys():
            navbar.set_icon(item['key'], item['icon'], item.get('only_icon', False))

    profile = conf.get('profile', [])
    for item in profile:
        if 'key' not in item.keys():
            RuntimeError('Profile items must have unique navbar key')

        if 'label' not in item.keys():
            RuntimeError('Profile items must have label')

        navbar.add_profile_item(
            item['key'],
            item['label'],
            item.get('url', None),
            item.get('type', None),
            item.get('controller', None),
            item.get('disabled', False)
        )

        if 'icon' in item.keys():
            navbar.set_icon(item['key'], item['icon'], item.get('only_icon', False))

    return navbar



class Navbar:
    NO_URL = 0
    URL_INTERNAL = 1
    URL_EXTERNAL = 2
    DIVIDER = 3
    URL_PARSED = 4

    def __init__(self):
        self._navbar = {'brand': {'brand_name': None, 'brand_html': None, 'brand_url': None}, 'items': [], 'profile': []}
        self._items = {}
        self._keys = []

    def set_brand(self, brand_name=None, brand_url=None, brand_html=None):
        self._navbar['brand']['brand_name'] = brand_name
        self._navbar['brand']['brand_url'] = brand_url
        self._navbar['brand']['brand_html'] = brand_html

    def set_active(self, key):
        item = self.get_item(key)
        item['active'] = True
        self._items[key] = item

    def set_icon(self, key, icon, only_icon=False):
        item = self.get_item(key)
        item['icon'] = icon
        item['only_icon'] = only_icon
        self._items[key] = item

    def add_menu_item(self, key, label, url=None, type=None, controller=None, disabled=False):
        self.__create_base_item(key, label, url, type, controller, disabled)
        self._items[key]['menus'] = []
        self._navbar['items'].append(key)

    def add_menu_sub_item(self, parent_key, key, label, url=None, type=None, controller=None, disabled=False):
        self.__create_base_item(key, label, url, type, controller, disabled)
        self._items[key]['parent'] = parent_key
        self._items[parent_key]['menus'].append(key)

    def add_profile_item(self, key, label, url=None, type=None, controller=None, disabled=False):
        self.__create_base_item(key, label, url, type, controller, disabled)
        self._navbar['profile'].append(key)

    def get_item(self, key):
        if key not in self._items:
            RuntimeError('This key: %s not exists' % key)
        return self._items[key]

    def get_data(self):
        return self._navbar

    def get_brand(self):
        return self._navbar['brand']

    def get_profile(self):
        profile = []
        for key in self._navbar['profile']:
            item = self.get_item(key)
            if item['type'] == self.URL_INTERNAL:
                item['url'] = url_for(item['url'])
                item['type'] = self.URL_PARSED
            profile.append(item)
        return profile

    def get_menu(self):
        menu = []
        for key in self._navbar['items']:
            item = self.get_item(key)
            if item['type'] == self.URL_INTERNAL:
                item['url'] = url_for(item['url'])
                item['type'] = self.URL_PARSED
            menu.append(item)
        return menu

    def __create_base_item(self, key, label, url=None, type=None, controller=None, disabled=False):
        self.__check_key(key)
        if type is None:
            type = self.NO_URL

        if type == self.NO_URL:
            url = '#'

        item = {'label': label, 'type': type, 'url': url, 'disabled': disabled, 'active': False, 'icon': None, 'only_icon': False}
        if controller is not None:
            item['controller'] = controller

        self._keys.append(key)
        self._items[key] = item

    def __check_key(self, key):
        if key in self._items:
            RuntimeError('This key: %s is not unique' % key)
        return True
