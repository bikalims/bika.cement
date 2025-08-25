
# -*- coding: utf-8 -*-

from AccessControl import ClassSecurityInfo
from bika.cement.interfaces import IBrand
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


class IBrandSchema(model.Schema):
    """Marker interface and Dexterity Python Schema for Brand"""

    # add basic things here
    title = schema.TextLine(
        title=u"Title",
        required=True,
    )

    description = schema.Text(
        title=u"Description",
        required=False,
    )



@implementer(IBrand, IBrandSchema, IDeactivable)
class Brand(Container):
    """Content-type class for IBrand"""

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
