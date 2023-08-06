Wagtail Global Settings
=========

Global settings editor for Wagtail using django-solo
---------

`wagtail-global-settings` provides a global singleton model editing
interface and frontend access for Wagtail. It uses [django-solo](https://github.com/lazybird/django-solo)
for the model.

Installation
----------

1. Install `wagtail-global-settings`.
2. Add `wagtail_global_settings` to `INSTALLED_APPS` in your `settings.py`. It should be after any
apps that use the `global_settings_tags` template tags.

Usage
----------

### Global settings

To use the global settings of `wagtail-global-settings` you need to define a model, which inherits
from `AbstractGlobalSettingsCollection`:

```python
from django.db import models
from wagtail.wagtailadmin.edit_handlers import FieldPanel
from wagtail_global_settings.models import AbstractGlobalSettingsCollection

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
```

For the frontend you have three options:

 * use the context processor:

   Add `'wagtail_global_settings.context_processors.global_settings'` to your `TEMPLATE_CONTEXT_PROCESSORS` and then use the
   settings in your template: `{{ global_settings.home.GlobalSettings.facebook_app_id }}`

 * use the template tags:

   Add `{% load global_settings_tags %}` at the beginning of your template and then use the tags in your template:
   `{% global_settings 'home' 'GlobalSettings' 'facebook_app_id' %}` or
   `{% get_global_settings 'home' 'GlobalSettings' 'facebook_app_id' as facebook_app_id %} {{ facebook_app_id }}`.
   It's possible to skip the field name, in which case you'll get the singleton model instance:
   `{% get_global_settings 'home' 'GlobalSettings' as global_settings %} {{ global_settings.facebook_app_id }}`

 * use the template tags provided by `django-solo`:

   Add `{% load solo_tags %}` at the beginning of your template and then use the tag in your template:
   `{% get_solo 'home.GlobalSettings' as global_settings %} {{ global_settings.facebook_app_id }}`

### Site specific settings

To use the site specific settings of `wagtail-global-settings` you need to define a model, which inherits
from `AbstractSiteSettingsCollection`:

```python
from django.db import models
from wagtail.wagtailadmin.edit_handlers import FieldPanel
from wagtail_global_settings.models import AbstractSiteSettingsCollection

class GlobalSettings(AbstractSiteSettingsCollection):
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
```

The usage is the same as with `AbstractGlobalSettingsCollection`, except:

* make sure `'wagtail.wagtailcore.middleware.SiteMiddleware'` is in `MIDDLEWARE_CLASSES`
* use `'wagtail_global_settings.context_processors.site_settings'` instead of
`'wagtail_global_settings.context_processors.global_settings'` and put it after
`'django.template.context_processors.request'` in `TEMPLATE_CONTEXT_PROCESSORS`
* use `{% load site_settings_tags %}` instead of `{% load global_settings_tags %}`
* use `{% site_settings %}` instead of `{% global_settings %}` in the template
* use `{% get_site_settings %}` instead of `{% get_global_settings %}` in the template
* `django-solo` cannot be used with site specific settings

The template tags for site specific settings allow passing and optional site argument:
`{% site_settings 'home' 'GlobalSettings' 'facebook_app_id' the_site %}`. If this
argument is missing the settings for the current site will be returned.

### Usage in views

For AbstractGlobalSettingsCollection:

```python
from home.models import GlobalSettings

def view_func_global(request):
    global_settings = GlobalSettings.get_solo()
    return render(request, 'home/the_template.html', {
        'facebook_app_id': global_settings.facebook_app_id,
    })
```

For AbstractSiteSettingsCollection:

```python
from home.models import GlobalSettings

def view_func_global(request):
    site_settings = GlobalSettings.objects.for_site(request.site)
    return render(request, 'home/the_template.html', {
        'facebook_app_id': site_settings.facebook_app_id,
    })
```

### General

The template tags may be used in two ways: `{% site_settings 'home' 'GlobalSettings' 'facebook_app_id' %}`
and `{% site_settings 'home.GlobalSettings.facebook_app_id' %}`.

For more information about configuration and caching see [django-solo](https://github.com/lazybird/django-solo).
