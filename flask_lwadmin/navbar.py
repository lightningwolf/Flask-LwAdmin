#!/usr/bin/env python
# coding=utf8
from flask_lwadmin import ConfigurationError
from flask import url_for


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

    def set_caret(self, key, caret):
        item = self.get_item(key)
        item['caret'] = caret
        self._items[key] = item

    def add_menu_item(self, key, label, url=None, type=None, credential=None, disabled=False):
        self.__create_base_item(key, label, url, type, credential, disabled)
        self._items[key]['dropdown'] = []
        self._navbar['items'].append(key)

    def add_profile_item(self, key, label, url=None, type=None, credential=None, disabled=False):
        self.__create_base_item(key, label, url, type, credential, disabled)
        self._items[key]['dropdown'] = []
        self._navbar['profile'].append(key)

    def add_group_item(self, parent_key, key, label, url=None, type=None, credential=None, disabled=False):
        self.__create_base_item(key, label, url, type, credential, disabled)
        self._items[key]['parent'] = parent_key
        self._items[key]['dropdown'] = []
        self._items[parent_key]['group'].append(key)

    def add_dropdown_item(self, parent_key, key, label, url=None, type=None, credential=None, disabled=False):
        self.__create_base_item(key, label, url, type, credential, disabled)
        self._items[key]['parent'] = parent_key
        self._items[parent_key]['dropdown'].append(key)

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

    def parse_item(self, item):
        if 'key' not in item.keys():
            ConfigurationError('Menu items must have unique key')

        if 'type' not in item.keys():
            item['type'] = self.NO_URL

        if 'group' in item.keys():
            item['label'] = ''
            item['type'] = self.GROUP

        if 'label' not in item.keys():
            ConfigurationError('Menu items must have label')

        item['caret'] = item.get('caret', False)

        return item

    def __create_base_item(self, key, label, url=None, type=None, credential=None, disabled=False):
        self.__check_key(key)
        if type is self.GROUP:
            self.__create_group_element(key)
        else:
            self.__create_normal_element(key, label, url, type, credential, disabled)

    def __create_group_element(self, key):
        item = {'type': self.GROUP, 'group': []}
        self._keys.append(key)
        self._items[key] = item

    def __create_normal_element(self, key, label, url, type, credential=None, disabled=False):
        if type == self.NO_URL:
            url = '#'

        item = {'label': label, 'type': type, 'url': url, 'disabled': disabled, 'active': False, 'icon': None, 'only_icon': False, 'hidden': False, 'caret': False}
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
            item = self.__prepare_item(self.get_item(key))
            if item['type'] == self.GROUP:
                item['group'] = self.__generate_group(item['group'])
            if len(item['dropdown']) > 0:
                item['dropdown'] = self.__generate_dropdown(item['dropdown'])

            result.append(item)
        return result

    def __generate_group(self, group):
        result = []
        for gkey in group:
            gitem = self.__prepare_item(self.get_item(gkey))
            if len(gitem['dropdown']) > 0:
                gitem['dropdown'] = self.__generate_dropdown(gitem['dropdown'])
            result.append(gitem)
        return result

    def __generate_dropdown(self, dropdowns):
        result = []
        for dropdown in dropdowns:
            item = self.__prepare_item(self.get_item(dropdown))
            result.append(item)
        return result

    def __prepare_item(self, item):
        if item['type'] == self.URL_INTERNAL:
            item['url'] = url_for(item['url'])
        return item


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
    item = navbar.parse_item(item)
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

    if item['caret']:
        navbar.set_caret(item['key'], True)

    if item['type'] == Navbar.GROUP:
        for subitem in item['group']:
            add_group_item(navbar, item['key'], subitem)

    if 'dropdown' in item.keys():
        for subitem in item['dropdown']:
            add_dropdown_item(navbar, item['key'], subitem)



def add_profile_item(navbar, item):
    item = navbar.parse_item(item)

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

    if item['caret']:
        navbar.set_caret(item['key'], True)

    if item['type'] == Navbar.GROUP:
        for subitem in item['group']:
            add_group_item(navbar, item['key'], subitem)

    if 'dropdown' in item.keys():
        for subitem in item['dropdown']:
            add_dropdown_item(navbar, item['key'], subitem)


def add_group_item(navbar, parent, item):
    item = navbar.parse_item(item)
    navbar.add_group_item(
        parent,
        item['key'],
        item['label'],
        item.get('url', None),
        item.get('type', None),
        item.get('credential', None),
        item.get('disabled', False)
    )

    if 'icon' in item.keys():
        navbar.set_icon(item['key'], item['icon'], item.get('only_icon', False))

    if item['caret']:
        navbar.set_caret(item['key'], True)

    if 'dropdown' in item.keys():
        for subitem in item['dropdown']:
            add_dropdown_item(navbar, item['key'], subitem)


def add_dropdown_item(navbar, parent, item):
    item = navbar.parse_item(item)
    navbar.add_dropdown_item(
        parent,
        item['key'],
        item['label'],
        item.get('url', None),
        item.get('type', None),
        item.get('credential', None),
        item.get('disabled', False)
    )

    if 'icon' in item.keys():
        navbar.set_icon(item['key'], item['icon'], item.get('only_icon', False))

    if item['caret']:
        navbar.set_caret(item['key'], True)
