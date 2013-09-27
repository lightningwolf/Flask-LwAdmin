#!/usr/bin/env python
# coding=utf8
__author__ = 'ldath'

from flask_lwadmin import ConfigurationError


class ConfigParser:
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
            if all(k in action for k in ("name", "label")):
                self.list_configuration['actions'].append(action)
            else:
                ConfigurationError('Wrong configuration format for list actions element')

    def parse_list_batch_actions(self, actions):
        pass

    def parse_list_object_actions(self, actions):
        pass

    def get_list_actions(self):
        return self.list_configuration.get('actions', None)

    def get_list_batch_actions(self):
        return self.list_configuration.get('batch_actions', None)

    def get_list_object_actions(self):
        return self.list_configuration.get('object_actions', None)
