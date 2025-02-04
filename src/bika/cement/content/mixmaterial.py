# -*- coding: utf-8 -*-

from AccessControl import ClassSecurityInfo
from bika.cement.interfaces import IMixMaterial
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


class IMixMaterialSchema(model.Schema):
    """Marker interface and Dexterity Python Schema for Mix Material"""

    # add basic things here
    title = schema.TextLine(
        title=u"Title",
        required=True,
    )

    description = schema.Text(
        title=u"Description",
        required=False,
    )

    specific_gravity = schema.Decimal(
        title=u"Specific Gravity",
        required=False,
    )

    absorption_rate = schema.Decimal(
        title=u"Absorption Rate",
        required=False,
    )

    manufacturer = UIDReferenceField(
        title=u"Manufacturer",
        allowed_types=("Manufacturer", ),
        multi_valued=False,
        required=False,
    )

    directives.widget(
        "supplier",
        UIDReferenceWidgetFactory,
        catalog=SETUP_CATALOG,
        query={
            "portal_type": "Supplier",
            "is_active": True,
            "sort_on": "sortable_title",
            "sort_order": "ascending",
        },
        limit=5,
    )

    supplier = UIDReferenceField(
        title=u"Supplier",
        allowed_types=("Supplier", ),
        multi_valued=False,
        required=False,
    )

    directives.widget(
        "material_type",
        UIDReferenceWidgetFactory,
        catalog=SETUP_CATALOG,
        query={
            "portal_type": "MaterialType",
            "is_active": True,
            "sort_on": "sortable_title",
            "sort_order": "ascending",
        },
        limit=5,
    )

    material_type = UIDReferenceField(
        title=u"Material Type",
        allowed_types=("MaterialType", ),
        multi_valued=False,
        required=False,
    )


@implementer(IMixMaterial, IMixMaterialSchema, IDeactivable)
class MixMaterial(Container):
    """Content-type class for IMixMaterial"""

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
