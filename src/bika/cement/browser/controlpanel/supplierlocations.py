# -*- coding: utf-8 -*-

import collections

from bika.cement.config import _
from bika.lims import api
from bika.lims.api import to_utf8
from bika.lims.utils import get_link
from senaite.app.listing import ListingView
from senaite.core.catalog import SETUP_CATALOG


class SupplierLocationsView(ListingView):
    """Displays all available sample containers in a table
    """

    def __init__(self, context, request):
        super(SupplierLocationsView, self).__init__(context, request)

        self.catalog = SETUP_CATALOG

        self.contentFilter = {
            "portal_type": "SupplierLocation",
            "sort_order": "ascending",
            "path": {
                "query": api.get_path(self.context),
            },
        }

        self.context_actions = {
            _("Add"): {
                "url": "++add++SupplierLocation",
                "icon": "++resource++bika.lims.images/add.png",
            }}

        t = self.context.translate
        self.title = t(_("Locations"))
        self.description = t(_(""))

        self.show_select_column = True
        self.pagesize = 25

        self.columns = collections.OrderedDict((
            ("supplier_location_title", {
                "title": _("Name"),
                "index": "sortable_title"}),
            ("address", {
                "title": _("Address"),
                "index": "description"}),
        ))

        self.review_states = [
            {
                "id": "default",
                "title": _("Active"),
                "contentFilter": {"is_active": True},
                "columns": self.columns.keys(),
            }, {
                "id": "inactive",
                "title": _("Inactive"),
                "contentFilter": {'is_active': False},
                "columns": self.columns.keys(),
            }, {
                "id": "all",
                "title": _("All"),
                "contentFilter": {},
                "columns": self.columns.keys(),
            },
        ]

    def folderitem(self, obj, item, index):
        """Service triggered each time an item is iterated in folderitems.
        The use of this service prevents the extra-loops in child objects.

        :obj: the instance of the class to be foldered
        :item: dict containing the properties of the object to be used by
            the template
        :index: current index of the item
        """
        obj = api.get_object(obj)

        location_link = get_link(
            obj.absolute_url(), obj.supplier_location_title
        )
        item["replace"]["supplier_location_title"] = location_link
        address_lst = []
        if obj.address and len(obj.address) > 0:
            address = obj.address[0]
            if address.get("address"):
                address_lst.append(to_utf8(address["address"]))
            if address.get("city"):
                address_lst.append(to_utf8(address["city"]))
            if address.get("zip"):
                address_lst.append(to_utf8(address["zip"]))
            if address.get("subdivision1"):
                address_lst.append(
                    to_utf8(address["subdivision1"]))
            if address.get("country"):
                address_lst.append(to_utf8(address["country"]))
        if address_lst:
            item["replace"]["address"] = get_link(
                href=api.get_url(obj), value=", ".join(address_lst)
            )

        return item
