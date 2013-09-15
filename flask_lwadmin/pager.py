#!/usr/bin/env python
# coding=utf8
from math import floor, ceil


class Pager:

    def __init__(self, max_per_page=10):
        self.page = 1
        self.max_per_page = max_per_page
        self.last_page = 1
        self.nb_results = 0
        self.current_max_link = 1
        self.max_record_limit = False
        self.offset = 0
        self.limit = max_per_page

    def initialize(self, count):
        has_max_record_limit = (self.get_max_record_limit() is not False)
        max_record_limit = self.get_max_record_limit()

        if has_max_record_limit:
            self.set_nb_results(min(count, max_record_limit))
        else:
            self.set_nb_results(count)

        page = self.get_page()
        if (0 == self.get_page()) or (0 == self.get_max_per_page()):
            self.set_last_page(0)
        else:
            self.set_last_page(int(ceil(self.get_nb_results() / float(self.get_max_per_page()))))
            self.offset = (page - 1) * self.get_max_per_page()
            if has_max_record_limit:
                max_record_limit -= self.offset
                if max_record_limit > self.get_max_per_page():
                    self.limit = self.get_max_per_page()
                else:
                    self.limit = max_record_limit
            else:
                self.limit = self.get_max_per_page()

    def get_offset(self):
        """Return offset for query"""
        return self.offset

    def get_limit(self):
        """Return limit for query"""
        return self.limit

    def get_max_record_limit(self):
        """Returns the current pager's max record limit."""
        return self.max_record_limit

    def set_max_record_limit(self, limit):
        """Sets the current pager's max record limit."""
        self.max_record_limit = limit

    def get_current_max_link(self):
        """Returns the current pager's max link"""
        return self.current_max_link

    def get_links(self, nb_links=5):
        """
        Returns an array of page numbers to use in pagination links.

        nb_links The maximum number of page numbers to return
        """
        page = self.page
        last_page = self.last_page
        links = []
        tmp = page - floor(nb_links / 2)
        check = last_page - nb_links + 1
        if check > 0:
            limit = check
        else:
            limit = 1

        if tmp > 0:
            if tmp > limit:
                begin = limit
            else:
                begin = tmp
        else:
            begin = 1

        i = int(begin)
        while (i < (begin + nb_links)) and (i <= last_page):
            links.append(i)
            i += 1

        if len(links):
            self.current_max_link = links[len(links) - 1]
        else:
            self.current_max_link = 1

        return links

    def have_to_paginate(self):
        """Returns true if the current query requires pagination."""
        if self.get_max_per_page() and self.get_nb_results() > self.get_max_per_page():
            return True
        return False

    def get_first_indice(self):
        """Returns the first index on the current page."""
        if self.page == 0:
            return 1
        else:
            return (self.page - 1) * self.max_per_page + 1

    def get_last_indice(self):
        """Returns the last index on the current page."""
        if self.page == 0:
            return self.nb_results
        else:
            if (self.page * self.max_per_page) >= self.nb_results:
                return self.nb_results
            else:
                return self.page * self.max_per_page

    def get_nb_results(self):
        """Returns the number of results."""
        return self.nb_results

    def set_nb_results(self, nb):
        """Sets the number of results."""
        self.nb_results = nb

    def get_first_page(self):
        """Returns the first page number."""
        return 1

    def get_last_page(self):
        """Returns the last page number."""
        return self.last_page

    def set_last_page(self, page):
        """Sets the last page number."""
        self.last_page = page
        if self.get_page() > page:
            self.set_page(page)

    def get_page(self):
        """Returns the current page."""
        return self.page

    def get_next_page(self):
        """Returns the next page."""
        return min((self.get_page() + 1), self.get_last_page())

    def get_previous_page(self):
        """Returns the previous page."""
        return max((self.get_page() - 1), self.get_first_page())

    def set_page(self, page):
        """Sets the current page."""
        self.page = int(page)

        if self.page <= 0:
            # set first page, which depends on a maximum set
            if self.get_max_per_page() > 0:
                self.page = 1
            else:
                self.page = 0

    def get_max_per_page(self):
        """Returns the maximum number of results per page."""
        return self.max_per_page

    def set_max_per_page(self, max):
        """Sets the maximum number of results per page."""
        if max > 0:
            self.max_per_page = max
            if self.page == 0:
                self.page = 1
        elif max == 0:
            self.max_per_page = 0
            self.page = 0
        else:
            self.max_per_page = 1
            if self.page == 0:
                self.page = 1

    def is_first_page(self):
        """Returns true if on the first page."""
        return 1 == self.page

    def is_last_page(self):
        """Returns true if on the last page."""
        return self.page == self.last_page

    def count(self):
        return self.nb_results
