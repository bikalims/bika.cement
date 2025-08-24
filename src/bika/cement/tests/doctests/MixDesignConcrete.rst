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
    >>> import transaction
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
    >>> setup = portal.setup
    >>> bikasetup = portal.bika_setup
    >>> current_file = os.path.dirname( __file__ )

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

    >>> mixtypes = setup.mixtypes
    >>> concrete = api.create(mixtypes, "MixType", title="Concrete")
    >>> concrete
    <MixType at /plone/setup/mixtypes/mixtype-1>
    >>> clients = portal.clients
    >>> client = clients.values()[0]
    >>> client
    <Client at /plone/clients/client-1>
    >>> spreadsheet_concrete = "files/ConcreteMix.xlsm"
    >>> file_path = os.path.join(current_file, '..', spreadsheet_concrete)
    >>> data = open(file_path, 'r').read()
    >>> import_file = FileUpload(TestFile(StringIO(data)))
    >>> batch = api.create(client, "Batch", MixSpreadsheet=data)
    >>> batch
    <Batch at /plone/clients/client-1/B-001>
    >>> messages = IStatusMessage(self.request).show()
    >>> [m.message for m in messages]
    [u'Spreadsheet Mix Materials not found: CEM-HCM1L, SLG-SKY, OZ-FE, 22CM11BLC, 27FM02MA, WR-82, LQFIBER, W1, W2']
    >>> mix_design = batch.values()[0]
    >>> mix_design
    <MixDesign at /plone/clients/client-1/B-001/mixdesign-1>
    >>> mix_design.title
    'Test-1'
    >>> mix_design.project
    'Test-0'
    >>> mix_design_concrete = mix_design.values()[0]
    >>> mix_design_concrete
    <MixDesignConcrete at /plone/clients/client-1/B-001/mixdesign-1/mixdesignconcrete-1>
    >>> mix_design_concrete.design
    0.43
    >>> mix_design_concrete.lab_temperature
    73
    >>> mix_design_concrete.design_slump
    4.5
