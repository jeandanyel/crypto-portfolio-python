#!/bin/sh

# Exit on error
set -e

# Run database migrations
echo "Applying database migrations..."
python manage.py migrate

# Check if the environment is development or production
if [ "$ENV" = "dev" ]; then
    echo "Starting Django development server..."
    python manage.py runserver 0.0.0.0:8000
else
    echo "Starting Gunicorn server..."
    gunicorn cryptofolio.wsgi:application --bind 0.0.0.0:8000
fi