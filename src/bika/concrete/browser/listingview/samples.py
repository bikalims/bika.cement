
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
        sample_name = [
            (
                "SampleName",
                {
                    "toggle": False,
                    "sortable": True,
                    "title": _("Sample Name"),
                },
            )
        ]
        material = [
            (
                "MixMaterial",
                {
                    "toggle": False,
                    "sortable": True,
                    "title": _("Material"),
                },
            )
        ]

        self.listing.columns.update(cast_date)
        self.listing.columns.update(curing_method)
        self.listing.columns.update(sample_name)
        self.listing.columns.update(material)

        for i in range(len(self.listing.review_states)):
            self.listing.review_states[i]["columns"].append("CastDate")
            self.listing.review_states[i]["columns"].append("CuringMethod")
            self.listing.review_states[i]["columns"].append("SampleName")
            self.listing.review_states[i]["columns"].append("MixMaterial")

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

        sample_name = obj.Schema()["SampleName"].getAccessor(obj)()
        if sample_name:
            item["SampleName"] = sample_name
        mix_material = obj.Schema()["MixMaterial"].getAccessor(obj)()
        if mix_material:
            mix_material_title = mix_material.title
            mix_material_url = mix_material.absolute_url()
            mix_material_link = get_link(
                mix_material_url, mix_material_title
            )
            item["MixMaterial"] = mix_material_title
            item["replace"]["MixMaterial"] = mix_material_link

        return item
