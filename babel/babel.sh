#!/bin/sh
pybabel extract -F babel.cfg -k _gettext -k _ngettext -k lazy_gettext -o messages.pot --project Flask-LwAdmin ../flask_lwadmin
