#!/bin/bash

# Install project dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --noinput

# Additional deployment steps or commands can be added here

# Run the project
python manage.py runserver
