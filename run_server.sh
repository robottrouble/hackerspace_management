python manage.py syncdb --noinput && chown www-data:www-data ./hackerspace_management.db && chmod 775 ./hackerspace_management.db && python manage.py runserver localhost:8000
