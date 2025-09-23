
# -*- coding: utf-8 -*-

from zope.component import adapts
from zope.interface import implements

from bika.lims import api
from bika.lims.browser import ulocalized_time
from senaite.app.listing.interfaces import IListingView
from senaite.app.listing.interfaces import IListingViewAdapter
from bika.concrete.config import _, is_installed
from bika.lims.utils import get_link


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

        curing_method = [
            (
                "CuringMethod",
                {
                    "toggle": False,
                    "sortable": True,
                    "title": _("Curing Method"),
                },
            )
        ]

        self.listing.columns.update(cast_date)
        self.listing.columns.update(curing_method)

        for i in range(len(self.listing.review_states)):
            self.listing.review_states[i]["columns"].append("CastDate")
            self.listing.review_states[i]["columns"].append("CuringMethod")

    def folder_item(self, obj, item, index):
        if not is_installed():
            return item
        obj = api.get_object(obj)
        cast_date = obj.Schema()["CastDate"].getAccessor(obj)()
        if cast_date:
            item["CastDate"] = ulocalized_time(cast_date, long_format=1)
        curing_method = obj.Schema()["CuringMethod"].getAccessor(obj)()
        if curing_method:
            curing_method_title = curing_method.title
            curing_method_url = curing_method.absolute_url()
            curing_method_link = get_link(
                curing_method_url, curing_method_title
            )
            item["CuringMethod"] = curing_method_title
            item["replace"]["CuringMethod"] = curing_method_link

        return item
