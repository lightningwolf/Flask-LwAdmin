#!/bin/sh
pybabel extract -F babel.cfg -k gettext -k ngettext -k lazy_gettext -o lw_admin.pot --project Flask-LwAdmin ../flask_lwadmin
