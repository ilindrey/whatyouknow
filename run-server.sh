#!/bin/bash

python manage.py migrate
python manage.py runserver [::]:8000
