Django Health
=============

Shows the health of your Django app easily. You don't need to make expensive requests to full pages. If your app
is up, this endpoint will work.

Quick Start
-----------

1. Install with pip:

    $ pip install django-health

2. Add 'health' to your INSTALLED_APPS setting:

    INSTALLED_APPS = (
        ...
        'health',
    )

3. Include the health URLconf in your project urls.py:

    url(r'^health/', include('health.urls')),

4. Start development server `python manage.py runserver`

5. Visit the health endpoint (http://127.0.0.1:8000/health/) for a `200 OK` to verify the site is up and that the
health endpoint is working.


