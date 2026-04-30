web: cd backend && gunicorn backend.wsgi:application --log-file - --bind 0.0.0.0:$PORT
release: cd backend && bash deploy.sh
