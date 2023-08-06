====
SUE
====

Theme for Mezzanine 3.1.10

1. Add "sue" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = (
        "sue",
        ....

# above other installed apps

2. Run "python manage.py schemamigration sue --initial" # Mezzanine 4+ "python manage.py makemigrations sue"

3. Run "python manage.py migrate sue" # Mezzanine 4+ "python manage.py migrate sue"

4. Change your URLs

5. Start dev server and log into the admin interface, select a skin in the settings, and save.


