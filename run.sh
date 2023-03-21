#!/usr/bin/with-contenv bashio

echo "Starting flask app!"

python3 -m flask --app main run --host=0.0.0.0 -p 8099 --debug

