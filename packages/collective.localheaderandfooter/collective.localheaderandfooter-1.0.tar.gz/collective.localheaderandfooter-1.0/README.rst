Introduction
============

.. image:: https://pypip.in/v/collective.localheaderandfooter/badge.png
    :target: https://pypi.python.org/pypi/collective.localheaderandfooter
    :alt: Latest PyPI version

.. image:: https://pypip.in/d/collective.localheaderandfooter/badge.png
    :target: https://pypi.python.org/pypi/collective.localheaderandfooter
    :alt: Number of PyPI downloads

.. image:: https://secure.travis-ci.org/jpgimenez/collective.localheaderandfooter.png
    :target: https://travis-ci.org/#!/jpgimenez/collective.localheaderandfooter

.. image:: https://coveralls.io/repos/jpgimenez/collective.localheaderandfooter/badge.png?branch=master
    :alt: Coverage
    :target: https://coveralls.io/r/jpgimenez/collective.localheaderandfooter?branch=master

This product allows you to apply custom header and/or footer to your Plone contents.

What it does
============

Registers a Dexterity behavior that you can enable on any content types and overrides `plone.header` and `plone.footer` viewlets.

Once enabled, on the edit page you'll find two new fields: `Custom header` and `Custom footer`.

You can select an item among the ones registered via Plone registry.

On save the selected header and/or footer will be applied on the content.

How to register a new header of footer
======================================

Create a `registry.xml` in you package's profile::

    <record name="localheaderandfooter.headers">
        <value purge="false">
        header-demo|Header demo
        header-free-account|Header free account
        </value>
    </record>

    <record name="localheaderandfooter.footers">
        <value purge="false">
        footer-light|Light footer
        </value>
    </value>

one item per line in the form `name|title`.

The `name` should match an existing view or page template, like::

    <browser:page
        for="*"
        name="header-demo"
        template="templates/header-demo.pt"
        permission="zope2.View"
        layer="..interfaces.ILayer"
        />

The latter will take precedence so that you can create them also from portal skins and override existing views.

Known bugs
==========

If you use this package you cannot override plone.header or plone.footer viewlets' template via `z3c.jbot` because your template will be not taken into account.

To override one of them you need to register a view w/ a template and call it `default-portal-header` or `default-portal-footer`::

    <browser:page
        for="*"
        name="default-portal-header"
        template="header.pt"
        permission="zope.Public"
        layer="..interfaces.ILayer"
        />

In this way you can also customize default header/footer per-content or per-marker interface.


Credits
=======

Authors:
--------

- Simone Orsi [simahawk] - Abstract srl
- Juan Pablo Giménez [jpgimenez]

Sponsor:
--------

* Sauce Labs https://saucelabs.com/
