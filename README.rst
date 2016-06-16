=================
Django Materialze
=================

This is a fork of [Django Material](https://github.com/viewflow/django-material). Sorry that we haven't really updated the README. We
wish to strip out the things that normally should be taken care of at the
project level, and also remove the frontend part, as we don't see the
benefit.

Material design for Django Forms and Admin. Template driven.

Overview
========

- Forms_ - New way to render django forms

  * Strong python/html code separation
  * Easy redefinition of particular fields rendering
  * Complex form layout support

- Admin_ - Material-designed django admin

Installation
============

django-materialize tested with Python 3.4/3.5, django 1.9::

.. pip install django-materialize


Forms
=====

Add `django_materialize` into INSTALLED_APPS settings

.. code-block:: python

    INSTALLED_APPS = (
         'django_materialize',
         ...
    )

Include django_materialize javascript and styles along with jQuery into your base template.

.. code-block:: html

    {% include 'django_materialize/includes/material_css.html' %}
    <script src="{% static 'django_materialize/js/jquery-2.2.0.js' %}"></script>
    {% include 'django_materialize/includes/material_js.html' %}

Load the `material_form` template tag library

.. code-block:: html

        {% load material_form %}

And render your form with {% form %} template tag

.. code-block:: html

    <form method="POST">
        {% csrf_token %}
        {% form form=form %}{% endform %}
        <button type="submit" name="_submit" class="btn">Submit</button>
    </form>

Template tags
-------------

`django-materialize` forms processing is built around simple concept
called *part*. `part` is like django template block, it has a default
value and could be overriden.  But `parts` are created dynamically for
each form field, which allows you to redefine specific form field html
render output.

Here is the example of rendering form with but prefix email field with email icon.

.. code-block:: html

    <form method="POST">
        {% csrf_token %}
        {% form %}
            {% part form.email prefix %}<div class="input-group-addon">@</div>{% endpart %}
        {% endform %}
        <button type="submit" name="_submit" class="btn">Submit</button>
    </form>

You can append value to of some tags attribute or completly override the attribute content.

.. code-block:: html

   {% form %}
       {% attr form.email 'group' class append %}yellow{% endattr %}
       {% attr form.email 'label' class append %}big{% endattr %}
       {% attr form.email 'widget' data-validate %}email{% endattr %} <!-- by default value would be overriden -->
       {% attr form.email 'widget' placeholder override %}{% endattr %}
   {% endform %}

There is a lot of other parts and attribute groups declared in default
templates. See template code for details.  If your widget is so
special, you can completly override its rendering

.. code-block:: html

    {% part form.my_field %}any html code here{% endpart %}


Layout
------

Layout object is the way to specify relative fields placements and sizes.

.. code-block:: python

    from django_materialize import *

    layout = Layout(
        Row('shipment_no', 'description')
        Fieldset("Add to inventory",
                 Row(Span3('product_name'), 'tags'),
                 Row('vendor', 'product_type'),
                 Row(Column('sku',
                            'stock_level',
                            span_columns=4),
                     'gender', 'desired_gender'),
                 Row('cost_price', Span2('wholesale_price'), 'retail_price')))

SpanXX elements are not to material grid classes, but used to
determine relative fields width. Each row occupies 12 grid columns.
Elements in Row('elem1', 'elem2') would be rendered in 6 grid coulmns
each, and in Row(Span2('elem1'), 'elem2') `elem1` would be rendered in
8 grid columns, and `elem2` in 4 grid columns.

Layouts rendering itself is specified in template.


ModelForm Views
---------------

Material forms library provides  LayoutMixin for model form views, populates
form fields list directly from layout object

.. code-block:: python

    from django import generic
    from viewform import LayoutMixin

    class SampleView(LayoutMixin, generic.ModelFormView):
        layout = Layout(...)

****

Admin
======

Add `django_materialize.admin` into INSTALLED_APPS settings

.. code-block:: python

    INSTALLED_APPS = (
         'django_materialize',
         'django_materialize.admin',
         ...
    )

*NOTE:* 'django_materialize.admin' must be added before 'django.contrib.admin'

Ensure that `django.template.context_processors.request` in your template context processor settings list

.. code-block:: python

    TEMPLATES = [
        {
            ...
            'OPTIONS': {
                'context_processors': [
                    ...
                    'django.core.context_processors.request',
                    ...
                ],
            },
        },
    ]

You can provide a custom admin site module in the `MATERIALIZE_ADMIN_SITE` setting

.. code-block:: python

    MATERIALIZE_ADMIN_SITE = 'mymodule.admin.admin_site'

**Admin support development is on initial stage. Only basic admin features are available.**
