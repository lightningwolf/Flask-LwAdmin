#!/usr/bin/env python
# coding=utf8
__author__ = 'ldath'

from flask import url_for
from flask_wtf import Form
from flask_lwadmin import ConfigurationError


class ConfigParser:
    NO_URL = 0
    URL_INTERNAL = 1
    URL_EXTERNAL = 2
    URL_CALL = 3
    HTML = 4

    def __init__(self):
        self.list_configuration = dict(
            id={},
            display=[],
            actions=[],
            object_actions=[],
            batch={},
            filter={}
        )

    def configure(self, configuration):
        if 'list' in configuration.keys():
            if 'display' in configuration['list'].keys():
                self.parse_list_display(configuration['list']['display'])

            if 'actions' in configuration['list'].keys():
                self.parse_list_actions(configuration['list']['actions'])

            if 'object_actions' in configuration['list'].keys():
                self.parse_list_object_actions(configuration['list']['object_actions'])

            if 'batch' in configuration['list'].keys():
                self.parse_batch(configuration['list']['batch'])

            if 'filter' in configuration['list'].keys():
                self.parse_filter(configuration['list']['filter'])

    def parse_list_display(self, elements):
        for element in elements:
            if not all(k in element for k in ('key', 'label')):
                raise ConfigurationError('Wrong configuration format for list display element')
            self.list_configuration['display'].append(element)

    def parse_list_actions(self, actions):
        for action in actions:
            parsed = self.parse_action(action)
            self.list_configuration['actions'].append(parsed)

    def parse_list_object_actions(self, actions):
        for action in actions:
            parsed = self.parse_action(action)
            self.list_configuration['object_actions'].append(parsed)

    def parse_action(self, action):
        if not all(k in action for k in ('key', 'label')):
            raise ConfigurationError('Wrong configuration format for list actions element')

        if 'type' not in action.keys():
            action['type'] = self.NO_URL

        if 'credential' not in action.keys():
            action['credential'] = None

        if 'confirm' not in action.keys():
            action['confirm'] = False

        if 'confirm_message' not in action.keys():
            action['confirm_message'] = 'Are you sure?'

        if 'class' not in action.keys():
            action['class'] = 'btn btn-small'

        if 'call' not in action.keys():
            action['call'] = False

        if 'visable' not in action.keys():
            action['visable'] = True

        if 'disabled' not in action.keys():
            action['disabled'] = False

        return action

    def parse_batch(self, batch_elemet):
        if not all(k in batch_elemet for k in ('url', 'form')):
            raise ConfigurationError('Wrong configuration format for list filter element')

        if 'type' not in batch_elemet.keys():
            batch_elemet['type'] = self.NO_URL

        self.list_configuration['batch'] = batch_elemet

    def parse_filter(self, filter_elemet):
        if not all(k in filter_elemet for k in ('url', 'form')):
            raise ConfigurationError('Wrong configuration format for list filter element')

        if 'type' not in filter_elemet.keys():
            filter_elemet['type'] = self.NO_URL

        self.list_configuration['filter'] = filter_elemet

    def is_list_actions(self):
        return True if self.list_configuration.get('actions', []) else False

    def get_pk(self):
        return self.list_configuration.get('pk')

    def get_list_display(self):
        return self.list_configuration.get('display', [])

    def get_list_actions(self):
        actions = self.list_configuration.get('actions', [])
        for action in actions:
            pre = action.copy()
            if pre['type'] == self.URL_INTERNAL:
                pre['url'] = url_for(pre['url'])

            yield pre

    def is_list_object_actions(self):
        return True if self.list_configuration.get('object_actions', []) else False

    def get_list_object_actions(self, call_object=None):
        actions = self.list_configuration.get('object_actions', [])
        for action in actions:
            pre = action.copy()
            if pre['type'] == self.URL_INTERNAL:
                pre['url'] = url_for(pre['url'])

            if pre['key'] == 'delete':
                pre['form'] = Form()

            if pre['call'] and call_object is not None:
                pre['type'] = self.URL_CALL
                pre = getattr(call_object, pre['call'])(pre)

            yield pre

    def is_batch(self):
        return True if self.list_configuration.get('batch', {}) else False

    def get_batch(self):
        batch_elemet = self.list_configuration.get('batch', {})

        pre = batch_elemet.copy()
        if pre['type'] == self.URL_INTERNAL:
            pre['url'] = url_for(pre['url'])
        return pre

    def is_filter(self):
        return True if self.list_configuration.get('filter', {}) else False

    def get_filter(self):
        filter_elemet = self.list_configuration.get('filter', {})

        pre = filter_elemet.copy()
        if pre['type'] == self.URL_INTERNAL:
            pre['url'] = url_for(pre['url'])
        return pre
