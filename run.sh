#!/usr/bin/with-contenv bashio

echo "Running migrations."
python3 -m flask db upgrade


echo "Starting flask app!"
python3 -m flask run --host=0.0.0.0 -p 8099 --debug

