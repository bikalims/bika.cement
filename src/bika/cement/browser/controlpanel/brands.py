# -*- coding: utf-8 -*-

import collections

from bika.cement.config import _
from bika.lims import api
from bika.lims.utils import get_link, get_link_for
from senaite.app.listing import ListingView
from senaite.core.catalog import SETUP_CATALOG


class BrandsView(ListingView):
    """Displays all available sample containers in a table
    """

    def __init__(self, context, request):
        super(BrandsView, self).__init__(context, request)

        self.catalog = SETUP_CATALOG

        self.contentFilter = {
            "portal_type": "Brand",
            "sort_order": "ascending",
        }

        self.context_actions = {
            _("Add"): {
                "url": "++add++Brand",
                "icon": "++resource++bika.lims.images/add.png",
            }}

        t = self.context.translate
        self.title = t(_("Brands"))
        self.description = t(_(""))

        self.show_select_column = True
        self.pagesize = 25

        self.columns = collections.OrderedDict((
            ("title", {
                "title": _("Title"),
                "index": "sortable_title"}),
            ("description", {
                "title": _("Description"),
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

        item["replace"]["title"] = get_link_for(obj)
        item["description"] = api.get_description(obj)

        return item
