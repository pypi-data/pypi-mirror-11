=============================
django-fractions
=============================

.. image:: https://badge.fury.io/py/django-fractions.png
    :target: https://badge.fury.io/py/django-fractions

.. image:: https://travis-ci.org/jmichalicek/django-fractions.png?branch=master
    :target: https://travis-ci.org/jmichalicek/django-fractions

Fraction display and form fields for Django

Documentation
-------------

The full documentation is at https://django-fractions.readthedocs.org.

Quickstart
----------

Install django-fractions::

    pip install django-fractions

Add ``djfractions`` to ``settings.INSTALLED_APPS``


Then use it in a project::

    import djfractions

In templates::

    {% load fractions %}
    {% display_fraction 1.25 %}

In Forms::

    from djfractions.forms import DecimalFractionField
    from django import forms

    class MyForm(forms.Form):
        a_fraction = DecimalFractionField()


Features
--------

* Template tag for displaying float and Decimal values as fractions including mixed numbers
* DecimalFractionField form field which handles input such as "1/4", "1 1/2", "1 and 1/2", and converts to a
  decimal.Decimal instance


TODO
-----

* Add unicode_fraction template tag to display the unicode fraction entity if available
* forms.FloatDecimalField to return a float rather than Decimal
* forms.SplitFractionWidget for having separate numerator and denominator form fields
* forms.SplitMixedFractionWidget for handling mixed number fractions with separate fields
* models.DecimalBackedFractionField() to store a Decimal value but return/accept it as a fraction
* models.FloatBackedFractionField() to store a Decimal value but return/accept it as a fraction


Cookiecutter Tools Used in Making This Package
----------------------------------------------

*  cookiecutter
*  cookiecutter-djangopackage




History
-------

0.3.2 (2015-08-28)
++++++++++++++++++

* Fixed boolean logic for when to coerce values to thirds in
  in forms.DecimalFractionField and get_fraction_parts()


0.3.1 (2015-08-12)
++++++++++++++++++

* HISTORY.rst typo fixes
* pypi release version fix

0.3.0 (2015-08-12)
++++++++++++++++++

* Added forms.FractionField which returns fractions.Fraction instances
* Refactoring of common code with new forms.FractionField
* Smarter checking for numeric types throughout the code
* forms.DecimalFractionField.to_python() handles fractions.Fraction values now
* Fixed bug handling negative numbers in quantity_to_decimal()
* Added min_value and max_value to forms.DecimalFractionField
* Made coerce_thirds, limit_denominator, and use_mixed_numbers params to DecimalFractionField
  proper named parameters and not just kwargs.

0.2.1 (2015-08-06)
++++++++++++++++++

* Fixed typo in usage docs

0.2.0 (2015-08-06)
++++++++++++++++++

* display_fraction template tag output is templated so that its formatting can be changed by users
* Added new display_improper_fraction template tag to simplify the common case of wanting to only use
  improper fractions with no whole numbers
* Added unicode_entity to template context for display_fraction and display_improper_fraction so that
  the html entity for common fractions may be used rather than <sup> and <sub> tags
* Refactored lots of code out into smaller, reusable functions
* Added a bunch of test cases

0.1.0 (2015-08-01)
++++++++++++++++++

* First release on PyPI.


