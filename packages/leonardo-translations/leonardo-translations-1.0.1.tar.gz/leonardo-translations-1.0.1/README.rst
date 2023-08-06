
=====================
Leonardo Translations
=====================

Integration of django-rosetta which eases the translation process of your Django projects.

.. contents::
    :local:

Features
--------

* Database independent
* Reads and writes your project’s gettext catalogs (po and mo files)
* Installed and uninstalled in under a minute
* Uses Django’s admin interface CSS

Installation
------------

.. code-block:: bash

    pip install leonardo-translations

.. code-block:: bash

    pip install django-leonardo[translations]

Navigate your browser to ``/admin/rosetta/``

Security
--------

Because Rosetta requires write access to some of the files in your Django project, access to the application is restricted to the administrator user only (as defined in your project’s Admin interface)

If you wish to grant editing access to other users::

    Create a ‘translators’ group in your admin interface
    Add the user you wish to grant translating rights to this group

Read More
---------

* https://github.com/django-leonardo/django-leonardo
* https://github.com/mbi/django-rosetta
