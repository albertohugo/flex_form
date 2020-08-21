release: python manage.py makemigrations
release: python manage.py migrate
release: python manage.py compilemessages
web: gunicorn setup.wsgi --log-file -