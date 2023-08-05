Django RQ Jobs
==============

Provides scheduled jobs management from the Django Admin using
`Django-RQ <https://github.com/ui/django-rq>`__

.. figure:: http://i.imgur.com/yd09EqH.png
   :alt: Admin Screenshot

   Admin Screenshot

Requirements
------------

-  `Django <https://www.djangoproject.com>`__
-  `Django-RQ <https://github.com/ui/django-rq>`__
-  `Arrow <https://github.com/crsmithdev/arrow>`__

Installation
------------

-  Make sure you have `Django-RQ <https://github.com/ui/django-rq>`__ up
   and running before you do anything. This app is just a simple admin
   plugin to manage your scheduled tasks and management commands.

-  Install the package with ``pip install django-rq-jobs``

-  Add ``django_rq_jobs`` to INSTALLED\_APPS in settings.py:

   .. code:: python

       INSTALLED_APPS = (
           # other apps
           "django_rq",
           "django_rq_jobs",
       )

-  Add ``RQ_JOBS_MODULE`` in settings.py. A string or a tuple of strings
   designating all modules where you keep your jobs. Anything marked
   with the Django RQ's ``@job`` decorator will show up in the admin.

   .. code:: python

       # A singe module:
       RQ_JOBS_MODULE = 'myapp.tasks'

       # or with multiple modules:
       RQ_JOBS_MODULE = (
           'myapp.tasks',
           'anotherapp.tasks',
       )

-  Run ``python manage.py migrate`` to create the job model.

-  Open your Django admin and find the RQ Jobs scheduled job section and
   schedule something.

-  Schedule the heartbeat ``python manage.py rqjobs`` with your favorite
   scheduler. This can be cron, Heroku scheduler or anything else you
   prefer. Make sure you set the heartbeat interval to something
   sensible; 5 or 10 minutes is usually enough, but run it every minute
   if you want. Execution of the jobs is deferred to RQ anyway.

Notes
-----

-  Supports once, hourly, daily, weekly, monthly, quarterly and yearly
   scheduled tasks.

-  Limited run schedules: Set the 'Repeats' on a task to the maxium
   number of repeats you want. The task gets deleted once the counter
   reaches zero. Defaults to ``-1`` for eternal.

-  Arguments are a dict: ``{'one': 1, 'two': 2, 'three': 3}``

-  RQ Jobs will try to link a job to a queue task status in Django RQ.
   Usually these job reports don't exist much longer than a few minutes
   unless they fail. So if you are seeing ``None`` in the RQ status,
   that usually means things went well.

-  If you haven't run the heartbeat ``manage.py rqjobs`` for a while and
   missed some scheduled jobs, RQ Jobs will play catch-up with every
   heartbeat. This way limited run schedules don't get compromised.

Scheduling Management Commands
------------------------------

If you want to schedule regular Django management commands, it's easiest
to add them using Django's management wrapper. So if you wanted to
schedule \`manage.py clearsessions' :

.. code:: python

    from django.core import management

    @job
    def clear_sessions():
        return management.call_command('clearsessions')

This will automagically appear as 'Clear Sessions' in the admin
interface.

Acknowledgements
----------------

Impossible without the excellent
`Django-RQ <https://github.com/ui/django-rq>`__ and
`RQ <https://github.com/nvie/rq>`__ projects. Thanks to
`Arrow <https://github.com/crsmithdev/arrow>`__ for making dates easy.
