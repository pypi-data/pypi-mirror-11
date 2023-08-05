=======================
Django Simple Blacklist
=======================

This application provide simple blacklist logic for django projects.
You can block specific IP-addresses and User Agents for accessing specific page or view-name per HTTP-method.
Also, you can configure rules to block users automatically after N requests per datetime.timedelta() and notify
site managers about clients which have been blocked!

Quick start
-----------

1. Add "blacklist" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = (
        ...
        'blacklist',
    )

2. Run `python manage.py migrate` to create the blacklists models.

3. Use blacklisting decorator for views which needs blacklisting logic like this::

    from blacklist.utils import blacklisting

    urlpatterns = (
        url(r'^view/$', blacklisting(log_requests=True)(my_view), name='log'),
    )

4. Configure AUTO_BLOCKING_RULES setting in your settings.py for auto-blocking logic::

    AUTO_BLOCKING_RULES = (
        {
            'RULE': {
                'ip': '.*',
            },
            'PERIOD': datetime.timedelta(days=1),
            'BLOCK_AFTER': 10,
            'ENABLED': True,
            'PROPOSAL': True,
            'NOTIFY': (
                ('Mikhail Nacharov', 'mnach@ya.ru'),
            )
        },
    )

  And call blacklist.models.RequestLog.objects.create_blocking_rules() periodically to
  create BlockRules. Please use cron via `django-cronjobs <https://pypi.python.org/pypi/django-cronjobs/0.2.3>`_
  or setup `django-celery <https://pypi.python.org/pypi/django-celery/3.1.16>`_ for this purpose.

5. If you need email notification configure django email settings as described in
https://docs.djangoproject.com/en/1.8/topics/email/. If you want to send users site
where blocking rules have been created you also need to enable and configure django
site framework: https://docs.djangoproject.com/en/1.8/ref/contrib/sites/

Requirements
------------

This package is compatible with Django 1.7 and 1.8 and can be ran on python 2.7 and higher.