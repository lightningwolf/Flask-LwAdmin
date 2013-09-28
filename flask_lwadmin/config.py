#!/usr/bin/env python
# coding=utf8
__author__ = 'ldath'

from flask import url_for
from flask_lwadmin import ConfigurationError


class ConfigParser:
    NO_URL = 0
    URL_INTERNAL = 1
    URL_EXTERNAL = 2
    URL_METHOD = 3

    def __init__(self):
        self.list_configuration = dict(actions=[], batch_actions=[], object_actions=[])

    def configure(self, configuration):
        if 'list' in configuration.keys():
            if 'actions' in configuration['list'].keys():
                self.parse_list_actions(configuration['list']['actions'])

            if 'batch_actions' in configuration['list'].keys():
                self.parse_list_batch_actions(configuration['list']['batch_actions'])

            if 'object_actions' in configuration['list'].keys():
                self.parse_list_object_actions(configuration['list']['object_actions'])

    def parse_list_actions(self, actions):
        for action in actions:
            parsed = self.parse_action(action)
            self.list_configuration['actions'].append(parsed)

    def parse_list_batch_actions(self, actions):
        for action in actions:
            parsed = self.parse_action(action)
            self.list_configuration['batch_actions'].append(parsed)

    def parse_list_object_actions(self, actions):
        for action in actions:
            parsed = self.parse_action(action)
            self.list_configuration['object_actions'].append(parsed)

    def parse_action(self, action):
        if not all(k in action for k in ('key', 'label')):
            ConfigurationError('Wrong configuration format for list actions element')

        if 'type' not in action.keys():
            action['type'] = self.NO_URL

        if 'credential' not in action.keys():
            action['credential'] = None

        if action['type'] == self.URL_INTERNAL:
            action['url'] = url_for(action['url'])

        return action

    def get_list_actions(self):
        return self.list_configuration.get('actions', [])

    def get_list_batch_actions(self):
        return self.list_configuration.get('batch_actions', [])

    def get_list_object_actions(self):
        return self.list_configuration.get('object_actions', [])
