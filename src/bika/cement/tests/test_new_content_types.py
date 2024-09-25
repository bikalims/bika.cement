# -*- coding: utf-8 -*-
#
# This file is part of BIKA.CEMENT
#
# Copyright 2018 by it's authors.


from bika.cement.content.curingmethods import ICuringMethods  # NOQA E501
from bika.cement.tests.base import SimpleTestCase
from plone import api
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import login
from plone.app.testing import setRoles


TITLE = "BIKA CEMENT NEW CONTENT TYPE TESTS"


class TestContentTypes(SimpleTestCase):

    def setUp(self):
        super(TestContentTypes, self).setUp()
        setRoles(self.portal, TEST_USER_ID, ["Member", "LabManager"])
        login(self.portal, TEST_USER_NAME)

    def test_add_curing_method(self):

        obj = api.content.create(
            container=self.portal,
            type='CuringMethods',
            id='curingmethods',
        )

        self.assertTrue(
            ICuringMethods.providedBy(obj),
            u'ICuringMethods not provided by {0}!'.format(
                obj.id,
            ),
        )

        parent = obj.__parent__
        self.assertIn('curingmethods', parent.objectIds())

        # check that deleting the object works too
        api.content.delete(obj=obj)
        self.assertNotIn('curingmethods', parent.objectIds())
