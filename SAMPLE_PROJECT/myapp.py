#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, render_template, url_for
from flask.ext.jqueryuibootstrap import Bootstrap
from flask.ext.lwadmin import LwAdmin, Navbar

app = Flask(__name__)
Bootstrap(app)

# LwAdmin
LwAdmin(app)

navbar = Navbar()
navbar.set_brand('Test Project')
navbar.set_username('anonymous')
navbar.add_item('app.homepage', 'Homepage', 'homepage', Navbar.URL_INTERNAL)
navbar.add_item('app.about', 'About', 'about', Navbar.URL_INTERNAL)
navbar.add_item('app.contact', 'Contact', 'contact', Navbar.URL_INTERNAL)


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
