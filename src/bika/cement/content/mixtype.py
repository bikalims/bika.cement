# -*- coding: utf-8 -*-

from AccessControl import ClassSecurityInfo
from bika.cement.interfaces import IMixType
from bika.lims.interfaces import IDeactivable
from plone.dexterity.content import Container
from plone.supermodel import model
from senaite.core.catalog import SETUP_CATALOG
from bika.lims import api
from zope import schema
from zope.interface import implementer


class IMixTypeSchema(model.Schema):
    """Marker interface and Dexterity Python Schema for Mix Types"""

    title = schema.TextLine(
        title=u"Title",
        required=True,
    )

    description = schema.Text(
        title=u"Description",
        required=False,
    )


@implementer(IMixType, IMixTypeSchema, IDeactivable)
class MixType(Container):
    """Content-type class for IMixType"""

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
