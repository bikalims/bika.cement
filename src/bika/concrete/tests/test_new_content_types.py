# -*- coding: utf-8 -*-
#
# This file is part of BIKA.CONCRETE
#
# Copyright 2018 by it's authors.


from bika.concrete.content.curingmethods import ICuringMethods
from bika.concrete.content.materialtypes import IMaterialTypes
from bika.concrete.content.mixtypes import IMixTypes
from bika.concrete.content.materialclasses import IMaterialClasses
from bika.concrete.content.mixmaterials import IMixMaterials
from bika.concrete.tests.base import SimpleTestCase
from plone import api
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import login
from plone.app.testing import setRoles


TITLE = "BIKA CONCRETE NEW CONTENT TYPE TESTS"


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

    def test_add_material_type(self):

        obj = api.content.create(
            container=self.portal,
            type='MaterialTypes',
            id='materialtypes',
        )

        self.assertTrue(
            IMaterialTypes.providedBy(obj),
            u'IMaterialTypes not provided by {0}!'.format(
                obj.id,
            ),
        )

        parent = obj.__parent__
        self.assertIn('materialtypes', parent.objectIds())

        # check that deleting the object works too
        api.content.delete(obj=obj)
        self.assertNotIn('materialtypes', parent.objectIds())

    def test_add_mix_types(self):

        obj = api.content.create(
            container=self.portal,
            type='MixTypes',
            id='mixtypes',
        )

        self.assertTrue(
            IMixTypes.providedBy(obj),
            u'IMixTypes not provided by {0}!'.format(
                obj.id,
            ),
        )

        parent = obj.__parent__
        self.assertIn('mixtypes', parent.objectIds())

        # check that deleting the object works too
        api.content.delete(obj=obj)
        self.assertNotIn('mixtypes', parent.objectIds())

    def test_add_material_classes(self):

        obj = api.content.create(
            container=self.portal,
            type='MaterialClasses',
            id='materialclasses',
        )

        self.assertTrue(
            IMaterialClasses.providedBy(obj),
            u'IMaterialClasses not provided by {0}!'.format(
                obj.id,
            ),
        )

        parent = obj.__parent__
        self.assertIn('materialclasses', parent.objectIds())

        # check that deleting the object works too
        api.content.delete(obj=obj)
        self.assertNotIn('materialclasses', parent.objectIds())

    def test_add_mix_materials(self):

        obj = api.content.create(
            container=self.portal,
            type='MixMaterials',
            id='mixmaterials',
        )

        self.assertTrue(
            IMixMaterials.providedBy(obj),
            u'IMixMaterials not provided by {0}!'.format(
                obj.id,
            ),
        )

        parent = obj.__parent__
        self.assertIn('mixmaterials', parent.objectIds())

        # check that deleting the object works too
        api.content.delete(obj=obj)
        self.assertNotIn('mixmaterials', parent.objectIds())
