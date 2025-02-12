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
    >>> from six import StringIO
    >>> from bika.lims import api
    >>> from DateTime import DateTime

    >>> from bika.cement.tests import test_setup
    >>> from zope.publisher.browser import FileUpload, TestRequest
    >>> from Products.statusmessages.interfaces import IStatusMessage

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
    >>> client = clients.values()[0]
    >>> client
    <Client at /plone/clients/client-1>
    >>> data = open(os.path.dirname( __file__ )+"/../files/ConcreteMix.xlsm", 'r').read()
    >>> import_file = FileUpload(TestFile(StringIO(data)))
    >>> batch = api.create(client, "Batch", MixSpreadsheet=data)
    >>> batch
    <Batch at /plone/clients/client-1/B-001>
    >>> messages = IStatusMessage(self.request).show()
    >>> [m.message for m in messages]
    [u'Spreadsheet Mix Type Concrete not found']
