====
SUE
====

Theme for Mezzanine 4.0.1

1. Add "sue" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = (
        "sue",
        ....

# above other installed apps

2. Run "python manage.py makemigrations"

3. Run "python manage.py migrate"

4. Change your URLs

5. Start dev server and log into the admin interface, select a skin in the settings, and save.

# uses Django migrations, make sure South is uninstalled


