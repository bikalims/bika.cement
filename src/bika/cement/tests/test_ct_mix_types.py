# -*- coding: utf-8 -*-
from bika.cement.content.mix_types import IMixTypes  # NOQA E501
from bika.cement.testing import BIKA_CEMENT_INTEGRATION_TESTING  # noqa
from plone import api
from plone.api.exc import InvalidParameterError
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.dexterity.interfaces import IDexterityFTI
from zope.component import createObject
from zope.component import queryUtility

import unittest




class MixTypesIntegrationTest(unittest.TestCase):

    layer = BIKA_CEMENT_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.parent = self.portal

    def test_ct_mix_types_schema(self):
        fti = queryUtility(IDexterityFTI, name='MixTypes')
        schema = fti.lookupSchema()
        self.assertEqual(IMixTypes, schema)

    def test_ct_mix_types_fti(self):
        fti = queryUtility(IDexterityFTI, name='MixTypes')
        self.assertTrue(fti)

    def test_ct_mix_types_factory(self):
        fti = queryUtility(IDexterityFTI, name='MixTypes')
        factory = fti.factory
        obj = createObject(factory)

        self.assertTrue(
            IMixTypes.providedBy(obj),
            u'IMixTypes not provided by {0}!'.format(
                obj,
            ),
        )

    def test_ct_mix_types_adding(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        obj = api.content.create(
            container=self.portal,
            type='MixTypes',
            id='mix_types',
        )

        self.assertTrue(
            IMixTypes.providedBy(obj),
            u'IMixTypes not provided by {0}!'.format(
                obj.id,
            ),
        )

        parent = obj.__parent__
        self.assertIn('mix_types', parent.objectIds())

        # check that deleting the object works too
        api.content.delete(obj=obj)
        self.assertNotIn('mix_types', parent.objectIds())

    def test_ct_mix_types_globally_addable(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        fti = queryUtility(IDexterityFTI, name='MixTypes')
        self.assertTrue(
            fti.global_allow,
            u'{0} is not globally addable!'.format(fti.id)
        )

    def test_ct_mix_types_filter_content_type_true(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        fti = queryUtility(IDexterityFTI, name='MixTypes')
        portal_types = self.portal.portal_types
        parent_id = portal_types.constructContent(
            fti.id,
            self.portal,
            'mix_types_id',
            title='MixTypes container',
        )
        self.parent = self.portal[parent_id]
        with self.assertRaises(InvalidParameterError):
            api.content.create(
                container=self.parent,
                type='Document',
                title='My Content',
            )
