# #!/bin/bash

# # Create and activate a virtual environment
# python3 -m venv myenv
# source myenv/bin/activate

# Install project dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic 

# # Additional deployment steps or commands can be added here

# # Deactivate the virtual environment
# deactivate

# # Run the project
# python manage.py runserver
