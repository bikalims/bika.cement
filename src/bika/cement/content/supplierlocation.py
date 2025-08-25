# -*- coding: utf-8 -*-

from AccessControl import ClassSecurityInfo
from Products.CMFCore import permissions
from plone.dexterity.content import Container
from plone.supermodel import model
from zope.interface import implementer
from zope.schema import TextLine

from bika.cement.config import _
from bika.cement.interfaces import ISupplierLocation
from bika.lims import api
from bika.lims.interfaces import IDeactivable
from senaite.core.catalog import SETUP_CATALOG
from senaite.core.schema import AddressField
from senaite.core.schema.addressfield import PHYSICAL_ADDRESS


class ISupplierLocationSchema(model.Schema):
    """Marker interface and Dexterity Python Schema for SupplierLocation"""

    supplier_location_title = TextLine(
        title=_("Name"),
        required=True,
    )

    address = AddressField(
        title=_("Address"),
        address_types=[PHYSICAL_ADDRESS],
    )


@implementer(ISupplierLocation, ISupplierLocationSchema, IDeactivable)
class SupplierLocation(Container):
    """Content-type class for ISupplierLocation"""

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
    def getAddress(self):
        """Returns the address"""
        accessor = self.accessor("address")
        return accessor(self)

    @security.protected(permissions.ModifyPortalContent)
    def setAddress(self, value):
        """Set address by the field accessor"""
        mutator = self.mutator("address")
        return mutator(self, value)

    @security.private
    def get_contacts_query(self):
        """Return the query for the account managers field"""
        return {
            "portal_type": "LabContact",
            "is_active": True,
            "sort_on": "title",
            "sort_order": "asscending",
        }
