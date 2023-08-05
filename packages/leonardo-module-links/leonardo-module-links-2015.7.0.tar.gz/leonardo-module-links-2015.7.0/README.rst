
==============
Leonardo Links
==============

Small module with ``Link`` and ``CategoryLink`` model and ``LinkButton`` and ``LinkMenu`` widgets for Leonardo

.. contents::
    :local:

Installation
------------

.. code-block:: bash

    pip install leonardo_module_links

or as leonardo bundle

.. code-block:: bash

    pip install django-leonardo["links"]

Add ``leonardo_module_links`` to APPS list, in the ``local_settings.py``::

    APPS = [
        ...
        'links'
        ...
    ]

    # or

    APPS = ['leonardo_module_links']
    
    # or

    INSTALLED_APPS = ['leonardo_module_links']       

Load new template to db

.. code-block:: bash

    python manage.py sync_all


See `Leonardo`_

.. _`Leonardo`: https://github.com/django-leonardo/django-leonardo