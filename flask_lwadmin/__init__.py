#!/usr/bin/env python
# coding=utf8

from flask import Blueprint, url_for


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


class Navbar(object):
    NO_URL = 0
    URL_INTERNAL = 1
    URL_EXTERNAL = 2
    DIVIDER = 3
    GROUP = 4

    def __init__(self):
        self._navbar = {'brand': {'brand_name': None, 'brand_html': None, 'brand_url': None}, 'items': [], 'profile': []}
        self._items = {}
        self._keys = []
        self._permissions = {}
        self.menu = []
        self.profile = []

    def set_permissions(self, permissions):
        self._permissions = permissions

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

    def add_menu_item(self, key, label, url=None, type=None, credential=None, disabled=False):
        self.__create_base_item(key, label, url, type, credential, disabled)
        self._items[key]['menus'] = []
        self._navbar['items'].append(key)

    def add_profile_item(self, key, label, url=None, type=None, credential=None, disabled=False):
        self.__create_base_item(key, label, url, type, credential, disabled)
        self._navbar['profile'].append(key)

    def add_group_item(self, parent_key, key, label, url=None, type=None, credential=None, disabled=False):
        pass

    def add_dropdown_item(self, parent_key, key, label, url=None, type=None, credential=None, disabled=False):
        self.__create_base_item(key, label, url, type, credential, disabled)
        self._items[key]['parent'] = parent_key
        self._items[parent_key]['menus'].append(key)

    def generate_menu(self):
        self.menu = self.__generate(self._navbar['items'])

    def generate_profile(self):
        self.profile = self.__generate(self._navbar['profile'])

    def get_item(self, key):
        if key not in self._items:
            ConfigurationError('This key: %s not exists' % key)
        return self._items[key]

    def get_data(self):
        return self._navbar

    def get_brand(self):
        return self._navbar['brand']

    def __create_base_item(self, key, label, url=None, type=None, credential=None, disabled=False):
        self.__check_key(key)
        if type is None:
            type = self.NO_URL

        if type is self.GROUP:
            self.__create_group_element(key)
        else:
            self.__create_normal_element(key, label, url, type, credential, disabled)

    def __create_group_element(self, key):
        item = {'type': self.GROUP, 'items': []}
        self._keys.append(key)
        self._items[key] = item

    def __create_normal_element(self, key, label, url, type, credential=None, disabled=False):
        if type == self.NO_URL:
            url = '#'

        item = {'label': label, 'type': type, 'url': url, 'disabled': disabled, 'active': False, 'icon': None, 'only_icon': False, 'hidden': False}
        if credential is not None and self._permissions is not None:
            if credential in self._permissions.keys():
                user_permissions = self._permissions[credential]
                item['hidden'] = self.__is_hidden(user_permissions)

        self._keys.append(key)
        self._items[key] = item

    def __check_key(self, key):
        if key in self._items:
            ConfigurationError('This key: %s is not unique' % key)
        return True

    def __is_hidden(self, user_permission=None):
        if user_permission is not None:
            if not user_permission.can():
                return True
        return False

    def __generate(self, data):
        result = []
        for key in data:
            item = self.get_item(key)
            print item
            if item['type'] == self.URL_INTERNAL:
                item['url'] = url_for(item['url'])
            result.append(item)
        return result


def create_navbar_fd(conf=None, active_key=None):
    """Creating navbar from dictionary type configuration"""

    conf = conf.copy() if conf else {}

    navbar = Navbar()
    brand = conf.get('brand', {})
    navbar.set_brand(
        brand_name=brand.get('brand_name', None),
        brand_url=brand.get('brand_url', None),
        brand_html=brand.get('brand_html', None)
    )
    if 'permissions' in conf.keys():
        navbar.set_permissions(conf['permissions'])

    items = conf.get('items', [])
    for item in items:
        add_menu_item(navbar, item)

    profile = conf.get('profile', [])
    for item in profile:
        add_profile_item(navbar, item)

    if active_key is not None:
        navbar.set_active(active_key)

    navbar.generate_menu()
    navbar.generate_profile()

    return navbar


def add_menu_item(navbar, item):
    if 'key' not in item.keys():
        ConfigurationError('Menu items must have unique key')

    if 'group' in item.keys():
        item['label'] = ''
        item['type'] = Navbar.GROUP

    if 'label' not in item.keys():
        ConfigurationError('Menu items must have label')

    navbar.add_menu_item(
        item['key'],
        item['label'],
        item.get('url', None),
        item.get('type', None),
        item.get('credential', None),
        item.get('disabled', False)
    )

    if 'icon' in item.keys():
        navbar.set_icon(item['key'], item['icon'], item.get('only_icon', False))


def add_profile_item(navbar, item):
    if 'key' not in item.keys():
        ConfigurationError('Profile items must have unique navbar key')

    if 'group' in item.keys():
        item['label'] = ''
        item['type'] = Navbar.GROUP

    if 'label' not in item.keys():
        ConfigurationError('Profile items must have label')

    navbar.add_profile_item(
        item['key'],
        item['label'],
        item.get('url', None),
        item.get('type', None),
        item.get('credential', None),
        item.get('disabled', False)
    )

    if 'icon' in item.keys():
        navbar.set_icon(item['key'], item['icon'], item.get('only_icon', False))
