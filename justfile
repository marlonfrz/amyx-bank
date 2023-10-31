runserver: _database
    python manage.py runserver

runserver0: _database
    python manage.py runserver 0.0.0.0:80

check:
    python manage.py check

shell: _database
    python manage.py shell

clean:
    find . -name '*.pyc' -exec rm {} \;

makemigrations app="": _database
    python manage.py makemigrations {{ app }}

showmigrations app="": _database
    python manage.py showmigrations {{ app }}

migrate app="": _database
    python manage.py migrate {{ app }}

startapp app:
    python manage.py startapp {{ app }}
