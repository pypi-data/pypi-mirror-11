Wagtail Plus
============

Wagtail Plus is a collection of independent modular add-ons for `Wagtail CMS <https://github.com/torchbox/wagtail>`_, featuring:

* ``wagtailplus.wagtaillinks``: Link storage and management for both external and email links. Fully integrated with Wagtail's WYSIWYG editor.

* ``wagtailplus.wagtailrelations``: Multi-faceted content relationship manager built around Wagtail's ``django-taggit`` implementation. Includes hierarchical site map.

Installation
~~~~~~~~~~~~
Wagtail Plus can be installed via ``pip`` using the following command::

    pip install wagtailplus

Once the Wagtail Plus package is installed, individual modules can be added to ``settings.INSTALLED_APPS`` as follows::

    INSTALLED_APPS = (
        ...
        'wagtailplus.wagtaillinks',
        'wagtailplus.wagtailrelations',
        ...
    )

After adding the desired modules to ``settings.INSTALLED_APPS``, run ``manage.py syncdb`` (Django < 1.7) or ``manage.py migrate`` (Django >= 1.7).

Documentation
~~~~~~~~~~~~~
Coming soon!