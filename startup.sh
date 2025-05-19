#!/bin/bash

# Instalacja Chromium
apt-get update && apt-get install -y chromium chromium-driver

# Uruchom Django przez Gunicorn
exec gunicorn cookie_scanner.wsgi:application --bind 0.0.0.0:$PORT --timeout 120
