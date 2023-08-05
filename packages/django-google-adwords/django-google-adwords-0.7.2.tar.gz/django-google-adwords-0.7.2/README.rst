=====================
django-google-adwords
=====================

`Django`_ modelling and helpers for the `Google Adwords API`_.

Using Celery_ to process tasks in the background the provided models include
methods to retrieve and store data for Accounts, Campaigns, Ad Groups and Ads to
your database for further processing.

Currently Google Adwords API version v201506_ is supported.

Installation
============

You can install django-google-adwords either via the Python Package Index (PyPI)
or from github.

To install using pip;

.. code-block:: bash

    pip install django-google-adwords

From github;

.. code-block:: bash

    pip install git+https://github.com/alexhayes/django-google-adwords.git


Settings
========

:code:`django-google-adwords` uses `django-appconf`_ to set default settings, of
which there are quite a lot. Out of the box you only need to set the required
settings however you will most likely want to change the Celery queues settings.

.. _`django-appconf`: http://django-appconf.readthedocs.org/en/latest/


Required
--------

You must place the following in your django settings file.

.. code-block:: python

	GOOGLEADWORDS_CLIENT_ID          = 'your-adwords-client-id'          # ie.. xyz123.apps.googleusercontent.com
	GOOGLEADWORDS_CLIENT_SECRET      = 'your-adwords-client-secret'      # xyz123xyz123xyz123xyz123
	GOOGLEADWORDS_REFRESH_TOKEN      = 'your-adwords-refresh-token'      # 1/xyz123xyz123xyz123xyz123xyz123xyz123xyz123x
	GOOGLEADWORDS_DEVELOPER_TOKEN    = 'your-adwords-developer-token'    # 1234567890
	GOOGLEADWORDS_CLIENT_CUSTOMER_ID = 'your-adwords-client-customer-id' # xyz123xyz123xyz123xyz1

If you don't know these values already you'll probably want to read the Google
Adwords `OAuth 2.0 Authentication`_ documentation.

.. _`OAuth 2.0 Authentication`: https://developers.google.com/adwords/api/docs/guides/authentication


Other Settings
--------------

Other settings can be found in :code:`django_google_adwords.settings` and can be
overridden by putting them in your settings file prepended with :code:`GOOGLEADWORDS_`.


Celery
------

Celery_ installation and configuration is somewhat out of the scope of this
document but in order to sync Google Adwords data into models you will need a
working Celery.

Essentially the syncing of data is a two step process, as follows;

1. Reports are downloaded from Adwords using the Celery queue specified in the 
setting :code:`GOOGLEADWORDS_REPORT_RETRIEVAL_CELERY_QUEUE`.
2. Downloaded reports are processed using the Celery queue specified in the 
setting :code:`GOOGLEADWORDS_DATA_IMPORT_CELERY_QUEUE`.  

By default the above two settings, along with :code:`GOOGLEADWORDS_HOUSEKEEPING_CELERY_QUEUE`
are set to :code:`celery` however you may want to spilt these up with different
workers, as follows;

.. code-block:: python

	GOOGLEADWORDS_REPORT_RETRIEVAL_CELERY_QUEUE = 'adwords_retrieval'
	GOOGLEADWORDS_DATA_IMPORT_CELERY_QUEUE = 'adwords_import'
	GOOGLEADWORDS_HOUSEKEEPING_CELERY_QUEUE = 'adwords_housekeeping'

With the above you could run the following workers;

.. code-block:: python

	celery worker --app myapp --queues adwords_retrieval &
	celery worker --app myapp --queues adwords_import &
	celery worker --app myapp --queues adwords_housekeeping &


.. _`Celery`: http://www.celeryproject.org


Usage
=====

Storing local data
------------------

The provided models include methods to sync data from the Google Adwords API to
the local models so that it can be queried at a later stage.

.. code-block:: python

	account_id = [YOUR GOOGLE ADWORDS ACCOUNT ID]
	account = Account.objects.create(account_id=account_id)
	result = account.sync() # returns a celery AsyncResult

Depending on the amount of data contained with your Adwords account the above
could take quite some time to populate! Advice is to monitor the celery task.

You can control what data is sync'd with the following settings:

.. code-block:: python

	GOOGLEADWORDS_SYNC_ACCOUNT = True    # Sync account data
	GOOGLEADWORDS_SYNC_CAMPAIGN = True   # Sync campaign data
	GOOGLEADWORDS_SYNC_ADGROUP = True    # Sync adgroup data
	GOOGLEADWORDS_SYNC_AD = False        # Sync ad data - note this can take a LOOOONNNNG time if you have lots of ads... 

Once you have created an account or have multiple accounts, you can, using
`Celery Beat`_ have the accounts sync'd at regular intervals by setting the
:code:`CELERYBEAT_SCHEDULE` similar to the following;

.. code-block:: python

	from celery.schedules import crontab
    CELERYBEAT_SCHEDULE = {
        'sync_google_adwords_data': {
            'task': 'django_google_adwords.tasks.sync_chain',
            'schedule': crontab(minute=5, hour=0),
        },
    }

.. _`Celery Beat`: http://celery.readthedocs.org/en/latest/userguide/periodic-tasks.html


Paged data
----------

To use the API but not store data in the models you can page through yielded data
with the following;

.. code-block:: python

	selector = {
	    'searchParameters': [
	        {
	            'xsi_type': 'RelatedToQuerySearchParameter',
	            'queries': ['seo', 'adwords', 'adwords seo']
	        },
	        {
	            'xsi_type': 'LanguageSearchParameter',
	            'languages': [{'id': '1000'}]
	        },
	        {
	            'xsi_type': 'LocationSearchParameter',
	            'locations': [{'id': '2036'}]
	        },
	    ],
	    'ideaType': 'KEYWORD',
	    'requestType': 'IDEAS',
	    'requestedAttributeTypes': ['KEYWORD_TEXT', 'SEARCH_VOLUME'],
	}
	
	for (data, selector) in paged_request('TargetingIdeaService', selector):
	    print data


Google Adwords API Versions
===========================

The intention is to keep in sync with the latest available Google Adwords API
versions - currently this is v201506_

To do this it's highly possible we'll need to break backwards compatibility as
the API can potentially do that.


Backwards Incompatibility Changes
=================================

v0.6.0
------

- Changed setting :code:`GOOGLEADWORDS_START_FINISH_CELERY_QUEUE` to :code:`GOOGLEADWORDS_HOUSEKEEPING_CELERY_QUEUE`.
- Removed :code:`Alert.sync_alerts()`, :code:`Alert.get_selector()` and task :code:`sync_alerts` as the services that these functions call have been discontinued in the Google API. The :code:`Alert` model remains in place so that existing alerts can be accessed if required.

v0.4.0
------

- Now using Django 1.7 migrations.
- Switched from money to djmoney (which itself uses py-moneyed).


Contributing
============

You are encouraged to contribute - please fork and submit pull requests. To get
a development environment up you should be able to do the following;

.. code-block:: bash

	git clone https://bitbucket.org/alexhayes/django-google-adwords.git
	cd django-google-adwords
	pip instal -r requirements/default.txt
	pip instal -r requirements/test.txt
	./runtests.py

And to run the full test suite, you can then run;

.. code-block:: bash

	tox

Note tox tests for Python 2.7, 3.3, 3.4 and PyPy for Django 1.7 and 1.8. 
You'll need to consult the docs for installation of these Python versions
on your OS, on Ubuntu you can do the following;

.. code-block:: bash

	sudo apt-get install python-software-properties
	sudo add-apt-repository ppa:fkrull/deadsnakes
	sudo apt-get update
	sudo apt-get install python2.7 python2.7-dev
	sudo apt-get install python3.3 python3.3-dev
	sudo apt-get install python3.4 python3.4-dev
	sudo apt-get install pypy pypy-dev

Note that :code:`django-nose` issue `#133`_ and `#197`_ cause issues with some 
tests thus the reason for `alexhayes/django-nose`_ being used in the 
:code:`requirements/test.py` and :code:`requirements/test3.py`.

.. _`#133`: https://github.com/django-nose/django-nose/issues/133
.. _`#197`: https://github.com/django-nose/django-nose/issues/197
.. _`alexhayes/django-nose`: https://github.com/alexhayes/django-nose  


Thanks
======

Thank-you to `roi.com.au`_ for supporting this project.

.. _`roi.com.au`: http://roi.com.au


Authors
=======

- Jeremy Storer <storerjeremy@gmail.com>
- Alex Hayes <alex@alution.com>

.. _`Django`: https://www.djangoproject.com/
.. _`Google Adwords API`: https://developers.google.com/adwords/api/
.. _`Celery`: http://www.celeryproject.org
.. _v201506: https://developers.google.com/adwords/api/docs/reference/#v201506
