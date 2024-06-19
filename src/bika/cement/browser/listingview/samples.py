
# -*- coding: utf-8 -*-

from zope.component import adapts
from zope.interface import implements

from bika.lims import api
from bika.lims.browser import ulocalized_time
from senaite.app.listing.interfaces import IListingView
from senaite.app.listing.interfaces import IListingViewAdapter
from bika.cement.config import _, is_installed


class SamplesListingViewAdapter(object):
    adapts(IListingView)
    implements(IListingViewAdapter)

    def __init__(self, listing, context):
        self.listing = listing
        self.context = context

    def before_render(self):
        if not is_installed():
            return

        cast_date = [
            (
                "CastDate",
                {
                    "toggle": False,
                    "sortable": True,
                    "title": _("Cast Date"),
                },
            )
        ]

        self.listing.columns.update(cast_date)
        for i in range(len(self.listing.review_states)):
            self.listing.review_states[i]["columns"].append("CastDate")

    def folder_item(self, obj, item, index):
        if not is_installed():
            return item
        obj = api.get_object(obj)
        cast_date = obj.Schema()["CastDate"].getAccessor(obj)()
        if cast_date:
            item["CastDate"] = ulocalized_time(cast_date, long_format=1)
        return item
