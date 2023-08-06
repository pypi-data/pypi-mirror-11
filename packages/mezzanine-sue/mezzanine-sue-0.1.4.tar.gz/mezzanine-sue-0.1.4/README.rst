====
SUE
====

Theme for Mezzanine 3.1.10

1. Add "sue" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = (
        "sue",
        ....

# above other installed apps

2. Run "python manage.py schemamigration sue --initial"

3. Run "python manage.py migrate sue" # in Mezzanine 4+ just run "python manage.py syncdb"

4. Change your URLs

5. Start dev server to check all is good


