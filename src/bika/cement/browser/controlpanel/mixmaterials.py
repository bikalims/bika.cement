# -*- coding: utf-8 -*-
#
# This file is part of SENAITE.CORE.
#
# SENAITE.CORE is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, version 2.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc., 51
# Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
# Copyright 2018-2023 by it's authors.
# Some rights reserved, see README and LICENSE.

import collections

from bika.cement.config import _
from bika.lims import api
from bika.lims.utils import get_link, get_link_for
from senaite.app.listing import ListingView
from senaite.core.catalog import SETUP_CATALOG


class MixMaterialsView(ListingView):
    """Displays all available sample containers in a table
    """

    def __init__(self, context, request):
        super(MixMaterialsView, self).__init__(context, request)

        self.catalog = SETUP_CATALOG

        self.contentFilter = {
            "portal_type": "MixMaterial",
            "sort_on": "sortable_title",
        }

        self.context_actions = {
            _("Add"): {
                "url": "++add++MixMaterial",
                "icon": "++resource++bika.lims.images/add.png",
            }}

        t = self.context.translate
        self.title = t(_("Mix Materials"))
        self.description = t(_(""))

        self.show_select_column = True
        self.pagesize = 25

        self.columns = collections.OrderedDict((
            ("title", {
                "title": _("Title"),
                "index": "sortable_title"}),
            ("material_type", {
                "title": _("Material Type"),
                "index": "material_type"}),
            ("manufacturer", {
                "title": _("Manufacturer"),
                "index": "sortable_title"}),
            ("supplier", {
                "title": _("Supplier"),
                "index": "sortable_title"}),
            ("description", {
                "title": _("Description"),
                "index": "description"}),
            ("specific_gravity", {
                "title": _("Specific Gravity"),
                "index": "specific_gravity"}),
            ("absorption_rate", {
                "title": _("Absorption Rate"),
                "index": "absorption_rate"}),
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
        item["specific_gravity"] = obj.specific_gravity
        item["absorption_rate"] = obj.absorption_rate

        # Manufacturer
        manufacturer_list = obj.manufacturer
        if manufacturer_list:
            manufacturer_obj = api.get_object_by_uid(manufacturer_list[0])
            manufacturer_title = manufacturer_obj.title
            manufacturer_url = manufacturer_obj.absolute_url()
            manufacturer_link = get_link(
                manufacturer_url, manufacturer_title
            )
            item["manufacturer"] = manufacturer_title
            item["replace"]["manufacturer"] = manufacturer_link

        # Supplier
        supplier_list = obj.supplier
        if supplier_list:
            supplier_obj = api.get_object_by_uid(supplier_list[0])
            supplier_title = supplier_obj.title
            supplier_url = supplier_obj.absolute_url()
            supplier_link = get_link(
                supplier_url, supplier_title
            )
            item["supplier"] = supplier_title
            item["replace"]["supplier"] = supplier_link

        # Material Type
        material_type_list = obj.material_type
        if material_type_list:
            material_type_obj = api.get_object_by_uid(material_type_list[0])
            material_type_title = material_type_obj.title
            material_type_url = material_type_obj.absolute_url()
            material_type_link = get_link(
                material_type_url, material_type_title
            )
            item["material_type"] = material_type_title
            item["replace"]["material_type"] = material_type_link

        return item
