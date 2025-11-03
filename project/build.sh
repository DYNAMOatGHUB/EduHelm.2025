#!/usr/bin/env bash
# exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --no-input

# Note: Djongo doesn't support migrations well with MongoDB
# So we skip migrate command
# python manage.py migrate

echo "Build completed successfully!"
