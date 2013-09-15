#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, render_template
from flask.ext.jqueryuibootstrap import JqueryUiBootstrap
from flask.ext.lwadmin import LwAdmin
from flask.ext.lwadmin.navbar import Navbar, create_navbar_fd

app = Flask(__name__)
JqueryUiBootstrap(app)

# LwAdmin
LwAdmin(app)

navbar_conf = {
    'brand': {'brand_name': 'Test Project', 'brand_url': '/'},
    'items': [
        {
            'key': 'app.homepage',
            'label': 'Homepage',
            'url': 'homepage',
            'type': Navbar.URL_INTERNAL
        },
        {
            'key': 'app.about',
            'label': 'About',
            'url': 'about',
            'type': Navbar.URL_INTERNAL
        },
        {
            'key': 'app.contact',
            'label': 'Contact',
            'url': 'contact',
            'type': Navbar.URL_INTERNAL
        }
    ],
    'profile': [
        {
            'key': 'profile.group',
            'group': [
                {
                    'key': 'lw_user',
                    'label': 'anonymous',
                    'icon': 'icon-user'
                },
                {
                    'key': 'lw_logout',
                    'label': 'logout',
                    'icon': 'icon-signout',
                    'only_icon': True
                }
            ]

        }
    ]
}


@app.route('/')
def homepage():
    navbar = create_navbar_fd(navbar_conf, 'app.homepage')
    return render_template('homepage.html', lw_navbar=navbar)


@app.route('/about')
def about():
    navbar = create_navbar_fd(navbar_conf, 'app.about')
    return render_template('about.html', lw_navbar=navbar)


@app.route('/contact')
def contact():
    navbar = create_navbar_fd(navbar_conf)
    navbar.set_active('app.contact')
    return render_template('contact.html', lw_navbar=navbar)


if __name__ == '__main__':
    app.run(debug=True)
