# -*- coding: utf-8 -*-

from AccessControl import ClassSecurityInfo
from Products.CMFCore import permissions
from plone.dexterity.content import Container
from plone.supermodel import model
from zope import schema
from zope.interface import Invalid
from zope.interface import implementer
from zope.interface import invariant

from bika.concrete.config import _
from bika.concrete.interfaces import IMaterialClass
from bika.lims import api
from bika.lims.interfaces import IDeactivable
from senaite.core.catalog import SETUP_CATALOG


class IMaterialClassSchema(model.Schema):
    """Marker interface and Dexterity Python Schema for MaterialClass"""

    title = schema.TextLine(
        title=u"Title",
        required=True,
    )

    description = schema.Text(
        title=u"Description",
        required=False,
    )

    sort_key = schema.Int(
        title=u"Sort Key",
        required=True,
    )

    @invariant
    def validate_sort_key(data):
        """Checks sort_key field for float value if exist
        """
        sort_key = getattr(data, "sort_key", None)
        if sort_key is None:
            return

        try:
            value = float(data.sort_key)
        except Exception:
            msg = _("Validation failed: value must be float")
            raise Invalid(msg)

        if value < 0 or value > 1000:
            msg = _("Validation failed: value must be between 0 and 1000")
            raise Invalid(msg)


@implementer(IMaterialClass, IMaterialClassSchema, IDeactivable)
class MaterialClass(Container):
    """Content-type class for IMaterialClass"""

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

    @security.protected(permissions.View)
    def getSortKey(self):
        accessor = self.accessor("sort_key")
        return accessor(self)

    @security.protected(permissions.ModifyPortalContent)
    def setSortKey(self, value):
        mutator = self.mutator("sort_key")
        mutator(self, value)

    # BBB: AT schema field property
    SortKey = property(getSortKey, setSortKey)
