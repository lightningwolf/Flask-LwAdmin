#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, render_template
from flask.ext.jqueryuibootstrap import Bootstrap
from flask.ext.lwadmin import LwAdmin, Navbar

app = Flask(__name__)
Bootstrap(app)

# LwAdmin
LwAdmin(app)

navbar = Navbar()
navbar.set_brand(brand_name='Test Project')
navbar.add_menu_item('app.homepage', 'Homepage', 'homepage', Navbar.URL_INTERNAL)
navbar.add_menu_item('app.about', 'About', 'about', Navbar.URL_INTERNAL)
navbar.add_menu_item('app.contact', 'Contact', 'contact', Navbar.URL_INTERNAL)
navbar.add_profile_item('lw_user', 'anonymous')
navbar.set_icon('lw_user', 'icon-user')
navbar.add_profile_item('lw_logout', 'logout')
navbar.set_icon('lw_logout', 'icon-signout', True)


@app.route('/')
def homepage():
    navbar.set_active('app.homepage')
    return render_template('homepage.html', lw_navbar=navbar)

@app.route('/about')
def about():
    navbar.set_active('app.about')
    return render_template('about.html', lw_navbar=navbar)

@app.route('/contact')
def contact():
    navbar.set_active('app.contact')
    return render_template('contact.html', lw_navbar=navbar)


if __name__ == '__main__':
    app.run(debug=True)
