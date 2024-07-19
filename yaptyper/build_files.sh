#!/bin/bash

VIRTUAL_ENV=venv

if [ -d "$VIRTUAL_ENV" ]; then
  source $VIRTUAL_ENV/bin/activate
fi

$(which pip) install -r requirements.txt

$(which python) manage.py collectstatic --noinput
