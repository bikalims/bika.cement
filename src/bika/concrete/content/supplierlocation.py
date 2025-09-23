# -*- coding: utf-8 -*-

from AccessControl import ClassSecurityInfo
from Products.CMFCore import permissions
from plone.autoform import directives
from plone.dexterity.content import Container
from plone.supermodel import model
from zope.interface import implementer
from zope.schema import TextLine

from bika.concrete.config import _
from bika.concrete.interfaces import ISupplierLocation
from bika.lims import api
from bika.lims.interfaces import IDeactivable
from senaite.core.catalog import SETUP_CATALOG
from senaite.core.catalog import CONTACT_CATALOG
from senaite.core.schema import AddressField
from senaite.core.schema.addressfield import PHYSICAL_ADDRESS
from senaite.core.schema import UIDReferenceField
from senaite.core.z3cform.widgets.uidreference import UIDReferenceWidgetFactory


class ISupplierLocationSchema(model.Schema):
    """Marker interface and Dexterity Python Schema for SupplierLocation"""

    supplier_location_title = TextLine(
        title=_("Title"),
        required=True,
    )

    directives.widget(
        "supplier_location_contact",
        UIDReferenceWidgetFactory,
        catalog=CONTACT_CATALOG,
        query="get_contacts_query",
        columns=[
            {
                "name": "title",
                "width": "30",
                "align": "left",
                "label": _(u"Title"),
            },
        ],
        limit=4,
    )
    supplier_location_contact = UIDReferenceField(
        title=_(u"Supplier Location Contact"),
        allowed_types=("SupplierContact",),
        multi_valued=False,
        description=_(u"Supplier Location Contact"),
        required=False,
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
        """Return the query for the supplier contact field"""
        return {
            "portal_type": "SupplierContact",
            "is_active": True,
            "sort_on": "title",
            "sort_order": "asscending",
            "path": {
                "query": api.get_path(self.aq_parent),
            },
        }
