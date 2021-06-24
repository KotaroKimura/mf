#!/bin/bash

WDIR=/app
cd $WDIR

uwsgi uwsgi.ini
# gunicorn application:application -b 0.0.0.0:8080 --reload --workers=1
