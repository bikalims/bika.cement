# -*- coding: utf-8 -*-

from AccessControl import ClassSecurityInfo
from bika.concrete.interfaces import IMaterialType
from bika.lims.interfaces import IDeactivable
from plone.dexterity.content import Container
from plone.supermodel import model
from plone.autoform import directives
from senaite.core.catalog import SETUP_CATALOG
from senaite.core.schema import UIDReferenceField
from bika.lims import api
from zope import schema
from zope.interface import implementer
from senaite.core.z3cform.widgets.uidreference import UIDReferenceWidgetFactory


class IMaterialTypeSchema(model.Schema):
    """Marker interface and Dexterity Python Schema for Material Types"""

    title = schema.TextLine(
        title=u"Title",
        required=True,
    )

    description = schema.Text(
        title=u"Description",
        required=False,
    )

    directives.widget(
        "material_class",
        UIDReferenceWidgetFactory,
        catalog=SETUP_CATALOG,
        query={
            "portal_type": "MaterialClass",
            "is_active": True,
            "sort_on": "sort_key",
            "sort_order": "ascending",
        },
        limit=5,
    )

    material_class = UIDReferenceField(
        title=u"Material Class",
        relationship="MaterialTypeMaterialClass",
        allowed_types=("MaterialClass", ),
        multi_valued=False,
        required=False,
    )


@implementer(IMaterialType, IMaterialTypeSchema, IDeactivable)
class MaterialType(Container):
    """Content-type class for IMaterialType"""

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
