#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, render_template
from flask.ext.jqueryuibootstrap import Bootstrap
from flask.ext.lwadmin import LwAdmin

app = Flask(__name__)
Bootstrap(app)

# LwAdmin
LwAdmin(app)


@app.route('/')
def index():
    return render_template('example.html')


if __name__ == '__main__':
    app.run(debug=True)
