#!/bin/bash

# Start the Docker containers in the background
echo "Starting database...."
docker compose up -d

# Wait for the database port to become active
echo "Waiting for database to be ready..."
while ! nc -z localhost 27017; do
  sleep 0.5
done

echo "Database is up! Starting Flask application...."
uv run flask run