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
navbar.set_brand('Test Project')
navbar.set_username('anonymous')
navbar.add_item('app.homepage', 'Homepage')
navbar.add_item('app.about', 'About')
navbar.add_item('app.contact', 'Contact')

print navbar.get_data()

@app.route('/')
def homepage():
    print navbar.get_menu()
    return render_template('homepage.html', lw_navbar=navbar)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html', lw_navbar=navbar)


if __name__ == '__main__':
    app.run(debug=True)
