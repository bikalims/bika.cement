# -*- coding: utf-8 -*-

from AccessControl import ClassSecurityInfo
from bika.concrete.interfaces import IMixMaterialAmount
from bika.lims.interfaces import IDeactivable
from plone.autoform import directives
from plone.dexterity.content import Container
from plone.supermodel import model
from senaite.core.catalog import SETUP_CATALOG
from senaite.core.z3cform.widgets.uidreference import UIDReferenceWidgetFactory
from bika.lims import api
from zope.interface import implementer
from zope import schema
from senaite.core.schema import UIDReferenceField


class IMixMaterialAmountSchema(model.Schema):
    """Marker interface and Dexterity Python Schema for Mix Material Amount"""

    directives.widget(
        "mix_material",
        UIDReferenceWidgetFactory,
        catalog=SETUP_CATALOG,
        query={
            "portal_type": "MixMaterial",
            "is_active": True,
            "sort_on": "sortable_title",
            "sort_order": "ascending",
        },
        limit=5,
    )

    mix_material = UIDReferenceField(
        title=u"Mix Material",
        allowed_types=("MixMaterial", ),
        multi_valued=False,
        required=False,
    )

    amounts = schema.Text(
        title=u"Amount",
        required=False,
    )

    moisture_corrected_batch_amounts = schema.Text(
        title=u"Moisture Corrected Batch Amounts",
        required=False,
    )

    mix_type_title = schema.Text(
        title=u"Mix Type Title",
        required=False,
    )


@implementer(IMixMaterialAmount, IMixMaterialAmountSchema, IDeactivable)
class MixMaterialAmount(Container):
    """Content-type class for IMixMaterialAmount"""

    _catalogs = [SETUP_CATALOG]

    security = ClassSecurityInfo()

    @security.private
    def accessor(self, fieldname):
        """Return the field accessor for the fieldname"""
        schema = api.get_schema(self)
        if fieldname not in schema:
            return None
        return schema[fieldname].get

    @security.private
    def mutator(self, fieldname):
        """Return the field mutator for the fieldname"""
        schema = api.get_schema(self)
        if fieldname not in schema:
            return None
        result = schema[fieldname].set
        self.reindexObject()
        return result
