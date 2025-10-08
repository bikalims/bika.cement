# -*- coding: utf-8 -*-

from AccessControl import ClassSecurityInfo
from plone.autoform import directives
from plone.dexterity.content import Container
from plone.supermodel import model
from zope.interface import implementer
from zope import schema

from bika.lims import api
from bika.lims.interfaces import IDeactivable
from senaite.core.catalog import SETUP_CATALOG
from senaite.core.z3cform.widgets.uidreference import UIDReferenceWidgetFactory
from senaite.core.schema import UIDReferenceField

from bika.concrete.config import _
from bika.concrete.interfaces import IMixMaterial


class IMixMaterialSchema(model.Schema):
    """Marker interface and Dexterity Python Schema for Mix Material"""

    title = schema.TextLine(
        title=_(
            u"title_mix_material_title",
            default=u"Title"
        ),
        description=_(
            u"description_mix_material_title",
            default=u"Title of the mixmaterial"
        ),
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
    directives.order_after(material_type='description')

    directives.widget(
        "brand",
        UIDReferenceWidgetFactory,
        catalog=SETUP_CATALOG,
        query={
            "portal_type": "Brand",
            "is_active": True,
            "sort_on": "sortable_title",
            "sort_order": "ascending",
        },
        limit=5,
    )

    brand = UIDReferenceField(
        title=u"Brand",
        allowed_types=("Brand", ),
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
