#!/bin/bash

$(which pip) install -r requirements.txt

$(which python) manage.py collectstatic --noinput
