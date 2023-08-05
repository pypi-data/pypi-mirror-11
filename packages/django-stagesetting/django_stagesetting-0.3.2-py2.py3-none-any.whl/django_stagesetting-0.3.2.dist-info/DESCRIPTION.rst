django-stagesetting 0.3.2
=========================

An application for managing site configuration through normal `Django`_ forms,
and thus through the `admin site`_.

Yay, I've made another app to abuse `contrib.admin`_.

.. |travis_stable| image:: https://travis-ci.org/kezabelle/django-stagesetting.svg?branch=0.3.2
  :target: https://travis-ci.org/kezabelle/django-stagesetting

.. |travis_master| image:: https://travis-ci.org/kezabelle/django-stagesetting.svg?branch=master
  :target: https://travis-ci.org/kezabelle/django-stagesetting

==============  ======
Release         Status
==============  ======
stable (0.3.2)  |travis_stable|
master          |travis_master|
==============  ======

Pre-requisites
--------------

The following versions are tested:

* Python 2.7, 3.3, or 3.4
* `Django`_ 1.7 or 1.8

Installation
------------

First up, you need to install it  (via `pip`_ as usual)::

    pip install django-stagesetting==0.3.2

Once that's downloaded, add the package to your ``INSTALLED_APPS``
in your settings::

    INSTALLED_APPS = (
        # ...
        'stagesetting',
        # ...
    )

do a migrate::

    python manage.py migrate stagesetting

Add a ``STAGESETTINGS`` dictionary to your project's settings::

    STAGESETTINGS = {
        'SETTING_NAME': '...',
        'ANOTHER_SETTING_NAME': '...',
    }

The setting collection name is the dictionary key, so must be unique.

Writing settings
^^^^^^^^^^^^^^^^
Settings may be created in a number of ways, the simplest of which is to
provide a ``dictionary`` as the value::

    STAGESETTINGS = {
        'MY_SETTING': {
            'an_example-datetime': datetime.today(),
            'a_date': date.today(),
            'time_now': time(4, 23),
            'boolean_field': False,
            'plain_text': 'char field',
            'decimal': Decimal('3.25'),
            'float': 2.3,
        }
    }

where possible, this will auto-generate a Form class for you, choosing sensible
defaults for the field variants where possible.

The other option is for the value to be a ``list`` or a ``tuple``, where
the *first item* represents a form (either a ``dictionary`` as above, **OR**
the ``dotted.path.to.a.Form.Class`` if you need custom validation) and the
*second, optional item* is the default data. The following should all be valid::

    STAGESETTINGS = {
        'AUTO_GENERATED': [{
            'datetime': datetime.today(),
        }],
        'IMPORT_A_FORM': ['myapp.forms.MyForm'],
        'IMPORT_WITH_DEFAULT': ['myapp.forms.MyForm', {'default': 'data'}],
        'AUTO_GENERATED_WITH_OTHER_DEFAULTS': [{
            'datetime': datetime.today(),
        }, {'default': 'data'}],
    }

A simple configuration form (for the ``dotted.path.Format``) might look like::

    from django.core.exceptions import ValidationError
    from django.forms import Form, DateField

    class DateForm(Form):
        start = DateField()
        end = DateField()

        def clean(self):
            cd = self.cleaned_data
            if 'start' in cd and 'end' in cd and cd['start'] > cd['end']:
                raise ValidationError("Start date cannot be after end date")
            return cd

As you can see, it really is just a normal `Form`_. Internally, this form's
``cleaned_data`` will be converted into `JSON`_ before being saved to the
database.
It will get re-converted to proper Python values when pulled out
of the database, by going through the given `Form`_ class's validation again,
including converting to rich values like model instances.


Python types which can be detected
**********************************

When detecting a dictionary as the value and auto-generating a form, the
following translations will be applied:

- ``None`` becomes `NullBooleanField`_
- ``datetime.datetime`` becomes `DateTimeField`_
- ``datetime.date`` becomes `DateField`_
- ``datetime.time`` becomes `TimeField`_
- ``datetime.timedelta`` becomes `DurationField`_
- ``decimal.Decimal`` becomes `DecimalField`_
- ``float`` becomes `FloatField`_
- ``True`` or ``False`` become `BooleanField`_
- ``int`` becomes `IntegerField`_
- ``uuid.UUID`` becomes `UUIDField`_ or `CharField`_, depending on the `Django`_ version
- ``list`` and ``tuple`` become `MultipleChoiceField`_
- ``collections.OrderedDict``, ``set``, ``frozenset``, and ``dict`` become `ChoiceField`_
- ``models.Model`` instances become `ModelChoiceField`_
- ``models.QuerySet`` becomes `ModelMultipleChoiceField`_
- strings become one of the following, depending on what checks they pass:

  - `GenericIPAddressField`_
  - `URLField`_
  - `EmailField`_
  - `SlugField`_
  - `CharField`_

Usage in code
-------------

The best way to access the settings in your views is to include
``stagesetting.middleware.ApplyRuntimeSettings`` in your ``MIDDLEWARE_CLASSES``
which will ensure there is a ``request.stagesettings`` variable which can be
used like so::

    def myview(request):
        how_many_form_data = request.stagesetting.LIST_PER_PAGE
        allow_empty_form_data = request.stagesetting['ALLOW_EMPTY']

each setting will be a dictionary of the `Form`_ values, either the default ones
or those changed in the database.

Usage in templates
------------------

If you've already got ``request`` in your template, obviously you can continue
to use ``request.stagesettings`` if the middleware is wired up.

If you don't have request, or you're not using the middleware,
``stagesetting.context_processors.runtime_settings`` provides a ``STAGESETTING``
template variable which contains the exact same data.

Usage outside of a request
--------------------------

If you don't have the middleware, or are in a part of the code which doesn't
have a ``request``, you can use the wrapper object directly::

    from stagesetting.models import RuntimeSettingWrapper
    def my_signal_handler(sender, instance, **kwargs):
        live_settings = RuntimeSettingWrapper()
        data = live_settings.LIST_PER_PAGE

Try to keep a single ``RuntimeSettingWrapper`` around for as long as possible,
rather than creating a new instance everywhere, as the object must fetch
the available settings from the database the first time it needs them. It
caches them for it's lifetime thereafter.


.. _Django: https://docs.djangoproject.com/en/stable/
.. _admin site: https://docs.djangoproject.com/en/stable/ref/contrib/admin/
.. _contrib.admin: https://docs.djangoproject.com/en/stable/ref/contrib/admin/
.. _Form: https://docs.djangoproject.com/en/stable/topics/forms/
.. _Forms: https://docs.djangoproject.com/en/stable/topics/forms/
.. _JSON: http://json.org/
.. _pip: https://pip.pypa.io/en/stable/
.. _pytest: http://pytest.org/latest/
.. _BooleanField: https://docs.djangoproject.com/en/stable/ref/forms/fields/#booleanfield
.. _CharField: https://docs.djangoproject.com/en/stable/ref/forms/fields/#charfield
.. _ChoiceField: https://docs.djangoproject.com/en/stable/ref/forms/fields/#choicefield
.. _DateField: https://docs.djangoproject.com/en/stable/ref/forms/fields/#datefield
.. _DateTimeField: https://docs.djangoproject.com/en/stable/ref/forms/fields/#datetimefield
.. _DecimalField: https://docs.djangoproject.com/en/stable/ref/forms/fields/#decimalfield
.. _DurationField: https://docs.djangoproject.com/en/stable/ref/forms/fields/#durationfield
.. _EmailField: https://docs.djangoproject.com/en/stable/ref/forms/fields/#emailfield
.. _FloatField: https://docs.djangoproject.com/en/stable/ref/forms/fields/#floatfield
.. _GenericIPAddressField: https://docs.djangoproject.com/en/stable/ref/forms/fields/#genericipaddressfield
.. _IntegerField: https://docs.djangoproject.com/en/stable/ref/forms/fields/#integerfield
.. _ModelChoiceField: https://docs.djangoproject.com/en/stable/ref/forms/fields/#modelchoicefield
.. _ModelMultipleChoiceField: https://docs.djangoproject.com/en/stable/ref/forms/fields/#modelmultiplechoicefield
.. _MultipleChoiceField: https://docs.djangoproject.com/en/stable/ref/forms/fields/#multiplechoicefield
.. _NullBooleanField: https://docs.djangoproject.com/en/stable/ref/forms/fields/#nullbooleanfield
.. _SlugField: https://docs.djangoproject.com/en/stable/ref/forms/fields/#slugfield
.. _TimeField: https://docs.djangoproject.com/en/stable/ref/forms/fields/#timefield
.. _URLField: https://docs.djangoproject.com/en/stable/ref/forms/fields/#urlfield
.. _UUIDField: https://docs.djangoproject.com/en/stable/ref/forms/fields/#uuidfield


----

License
-------

``django-stagesetting 0.3.2`` is available under the terms of the
Simplified BSD License (alternatively known as the FreeBSD License, or
the 2-clause License)::

    Copyright (c) 2015, Keryn Knight
    All rights reserved.

    Redistribution and use in source and binary forms, with or without
    modification, are permitted provided that the following conditions are met:

    1. Redistributions of source code must retain the above copyright notice, this
       list of conditions and the following disclaimer.
    2. Redistributions in binary form must reproduce the above copyright notice,
       this list of conditions and the following disclaimer in the documentation
       and/or other materials provided with the distribution.

    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
    ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
    WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
    DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
    ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
    (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
    LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
    ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
    (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
    SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

    The views and conclusions contained in the software and documentation are those
    of the authors and should not be interpreted as representing official policies,
    either expressed or implied, of the FreeBSD Project.


----

Change log
----------
0.3.2
^^^^^^

* Fixed error introduced in ``0.3.1`` when only providing a dictionary, because
  it turns out it wasn't being covered by tests.

0.3.1
^^^^^^

* Fixed issue where providing a dictionary wasn't treating the values as
  implicit defaults to be created into the database.


0.3.0
^^^^^^

* Added ability to auto-generate forms for configuration values which are
  dictionaries.

0.2.0
^^^^^^

* Initial release.



