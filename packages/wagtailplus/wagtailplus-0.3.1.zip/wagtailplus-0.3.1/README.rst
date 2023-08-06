Wagtail Plus
============

Wagtail Plus is a collection of independent modular add-ons for `Wagtail CMS <https://github.com/torchbox/wagtail>`_, featuring:

* ``wagtailplus.wagtaillinks``: Link storage and management for both email addresses and external URLs. Fully integrated with Wagtail's rich-text editor.

* ``wagtailplus.wagtailrelations``: Multi-faceted content relationship manager built around Wagtail's implementation of ``django-taggit``. Includes views and templates for a hierarchical site map.

* ``wagtailplus.wagtailrollbacks``: Version control manager that includes the ability to "rollback" or revert to a previous version of a page.

Installation
~~~~~~~~~~~~
Wagtail Plus can be installed via ``pip`` using the following command::

    pip install wagtailplus

Once the Wagtail Plus package is installed, individual modules can be added to ``settings.INSTALLED_APPS`` as follows::

    INSTALLED_APPS = (
        ...
        'wagtailplus.wagtaillinks',
        'wagtailplus.wagtailrelations',
        'wagtailplus.wagtailrollbacks',
        ...
    )

After adding the desired modules to ``settings.INSTALLED_APPS``, run ``manage.py syncdb`` (Django < 1.7) or ``manage.py migrate`` (Django >= 1.7).

Documentation
~~~~~~~~~~~~~
The latest documentation is available at `wagtailplus.readthedocs.org <http://wagtailplus.readthedocs.org/en/latest/index.html>`_.