#!/usr/bin/env python
# coding=utf8
__author__ = 'ldath'


class ConfigParser:

    def __init__(self):
        self.list_configuration = {'batch_actions': None, 'object_actions': None}

    def configure(self):
        if 'batch_actions' in self.list_configuration.keys():
            self.parse_batch_actions()

        if 'object_actions' in self.list_configuration.keys():
            self.parse_object_actions()

    def parse_batch_actions(self):
        pass

    def parse_object_actions(self):
        pass

    def get_batch_actions(self):
        return self.list_configuration.get('batch_actions', None)

    def get_object_actions(self):
        return self.list_configuration.get('object_actions', None)
