# -*- coding: utf-8 -*-
#
# This file is part of BIKA.CEMENT
#
# Copyright 2018 by it's authors.


from bika.cement.content.curingmethod import ICuringMethod  # NOQA E501

from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import login
from plone.app.testing import setRoles

from bika.cement.tests.base import BaseTestCase



from plone import api


TITLE = "BIKA CEMENT NEW CONTENT TYPE TESTS"


class TestSoftware(BaseTestCase):

    def setUp(self):
        super(TestSoftware, self).setUp()
        setRoles(self.portal, TEST_USER_ID, ["Member", "LabManager"])
        login(self.portal, TEST_USER_NAME)

        self.client = self.add_client(title="Happy Hills", ClientID="HH")

        self.contact = self.add_contact(
            self.client, Firstname="Rita", Surname="Mohale"
        )

    def test_add_curing_method(self):
        import pdb;pdb.set_trace()
        from bika.lims import api as bika_api
        setup = bika_api.get_senaite_setup()
        obj = api.content.create(
            container=self.portal,
            type='CuringMethod',
            id='curingmethod',
        )

        self.assertTrue(
            ICuringMethod.providedBy(obj),
            u'IExample not provided by {0}!'.format(
                obj.id,
            ),
        )

        parent = obj.__parent__
        self.assertIn('curingmethod', parent.objectIds())

        # check that deleting the object works too
        api.content.delete(obj=obj)
        self.assertNotIn('curingmethod', parent.objectIds())
