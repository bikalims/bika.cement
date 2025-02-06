BIKA CEMENT CONCRETE MIX
========================

Import and export instrument adapters for SENAITE

Running this test from the buildout directory::

    bin/test -s bika.cement test_doctests -t MixDesignConcrete


Test Setup
----------
Needed imports::

    >>> import os
    >>> import cStringIO
    >>> from bika.lims import api
    >>> from DateTime import DateTime

    >>> from bika.cement.tests import test_setup
    >>> from zope.publisher.browser import FileUpload, TestRequest

Functional helpers::

    >>> def timestamp(format="%Y-%m-%d"):
    ...     return DateTime().strftime(format)

    >>> class TestFile(object):
    ...     def __init__(self, file, filename='dummy.txt'):
    ...         self.file = file
    ...         self.headers = {}
    ...         self.filename = filename

Variables::

    >>> date_now = timestamp()
    >>> portal = self.portal
    >>> request = self.request

We need certain permissions to create and access objects used in this test,
so here we will assume the role of Lab Manager::

    >>> from plone.app.testing import TEST_USER_ID
    >>> from plone.app.testing import setRoles
    >>> setRoles(portal, TEST_USER_ID, ['Manager',])


Import test
-----------

Required steps: Create Batch and upload concrete mix spreadsheet
................................................................

A `MixDesign` can only be created inside a `Batch`, a `MixDesignConcrete` is 
is created on a `MixDesign`::

    >>> clients = self.portal.clients
    >>> client = api.create(clients, "Client", Name="NARALABS", ClientID="NLABS")
    >>> client
    <Client at /plone/clients/client-1>
    >>> contact = api.create(client, "Contact", Firstname="Juan", Surname="Gallostra")
    >>> contact
    <Contact at /plone/clients/client-1/contact-1>
    >>> batch = api.create(client, "Batch")
    >>> batch
    <Batch at /plone/clients/client-1/B-001>
