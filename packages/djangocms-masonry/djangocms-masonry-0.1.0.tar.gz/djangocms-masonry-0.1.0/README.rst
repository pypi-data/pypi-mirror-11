djangocms-masonry
=================

**djangocms-masonry** is a reuseable plugin for `django-cms` that
implements the JavaScript Masonry library.

Dependencies
------------

-  Djangocms>=3.0
-  Django>=1.6

Installation
------------

Install djangocms-masonry from Pypi.

.. code:: python

    pip install djangocms-masonry

Add Djangocms\_masonry to INSTALLED\_APPS

.. code:: python

    INSTALLED_APPS = (
        ...
        'djangocms_masonry',
        ...
    )

Django 1.6 and/or South users will need to add the following to ensure
migration compatibility.

.. code:: python

    SOUTH_MIGRATION_MODULES = {
        ...
        'djangocms_masonry': 'djangocms_masonry.south_migrations',
        ...
    }

Configuration
-------------

CSS classes can be added to the plugin via a select box by using the
**DJANGOCMS\_MASONRY\_STYLES** settings tuple.

.. code:: python

    DJANGOCMS_MASONRY_STYLES = (
        ('style1', 'Style 1'),
        ('style2', 'Style 2'),
    )

djangocms\_masonry/default.html is rendered by default. The user can select
custom templates if the following tuple is set as the example below
demonstrates.

.. code:: python

    DJANGOCMS_MASONRY_TEMPLATES = (
        ('template1', 'Template 1'),
        ('template2', 'Template 2'),
    )


Restrict the plugins available to Masonry Carousel

.. code:: python

    DJANGOCMS_MASONRY_CHILD_CLASSES = (
        'PicturePlugin',
    )

Include or exclude static files

.. code:: python

    DJANGOCMS_MASONRY_INCLUDE_JS_MASONRY = True


Templates
---------

base.html includes all the JavaScript and CSS needed to run the masonry plugin, but it does not render the HTML.
Custom templates can extend base.html as long as they define a plugin block containing the html and plugin render code as show in the below example.

.. code:: html

    {% extends 'djangocms_masonry/base.html' %}
    {% load cms_tags %}

    {% block plugin %}
      <div class="masonry-plugin plugin{% if style %} {{ style }}{% endif %}" id="plugin-{{ instance.pk }}">
        <div class="row">
          <div class="small-12 columns">

            <div class="masonry-grid">
              <div class="grid-sizer"></div>
              <div class="gutter-sizer"></div>
              {% for plugin in instance.child_plugin_instances %}
                <div class="grid-item">
                  {% render_plugin plugin %}
                </div>
              {% endfor %}
            </div>

          </div>
        </div>
      </div>
    {% endblock plugin %}

Contributions
-------------

-  Lee Solway

History
-------

**0.1.0** (2015-07-24)

- First release on PyPI

