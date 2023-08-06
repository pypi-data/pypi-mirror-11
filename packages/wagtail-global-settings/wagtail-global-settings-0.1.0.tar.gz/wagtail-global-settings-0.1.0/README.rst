Wagtail Global Settings
=======================

Global settings editor for Wagtail using django-solo
----------------------------------------------------

``wagtail-global-settings provides`` provides a global singleton model
editing interface and frontend access for Wagtail. It uses
`django-solo <https://github.com/lazybird/django-solo>`__ to for the
model.

Installation
------------

1. Install ``wagtail-global-settings``.
2. Add ``wagtail_global_settings`` to ``INSTALLED_APPS`` in your
   ``settings.py``. It should be after any apps that use the
   ``global_settings_tags`` template tags.

Usage
-----

To use ``wagtail-global-settings`` you need to define a model, which
inherits from ``AbstractGlobalSettingsCollection``:

.. code:: python

    class GlobalSettings(AbstractGlobalSettingsCollection):
        facebook_app_id = models.CharField(max_length=256)
        google_app_id = models.CharField(max_length=256)
        analytics_id = models.CharField(max_length=256)
        
        panels = [
            FieldPanel('facebook_app_id'),
            FieldPanel('google_app_id),
            FieldPanel('analytics_id'),
        ]
        
        class Meta:
            verbose_name = "Global settings"

For the frontend you have three options:

-  use the context processor:

Add ``'wagtail_global_settings.context_processors.global_settings'`` to
your ``TEMPLATE_CONTEXT_PROCESSORS`` and then use the settings in your
template: ``{{ global_settings.home.GlobalSettings.facebook_app_id }}``

-  use the template tags:

Add ``{% load global_settings_tags %}`` at the beginning of your
template and then use the tags in your template:
``{% global_settings 'home' 'GlobalSettings' 'facebook_app_id' %}`` or
``{% get_global_settings 'home' 'GlobalSettings' 'facebook_app_id' as facebook_app_id %} {{ facebook_app_id }}``.
It's possible to skip the field name, in which case you'll get the
singleton model instance:
``{% get_global_settings 'home' 'GlobalSettings' as global_settings %} {{ global_settings.facebook_app_id }}``

-  use the template tags provided by ``django-solo``:

Add ``{% load solo_tags %}`` at the beginning of your template and then
use the tag in your template:
``{% get_solo 'home.GlobalSettings' as global_settings %} {{ global_settings.facebook_app_id }}``

For more information about configuration and caching see
`django-solo <https://github.com/lazybird/django-solo>`__.
