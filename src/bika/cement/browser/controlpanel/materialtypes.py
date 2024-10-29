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


class MaterialTypesView(ListingView):
    """Displays all available material types in a table"""

    def __init__(self, context, request):
        super(MaterialTypesView, self).__init__(context, request)

        self.catalog = SETUP_CATALOG

        self.contentFilter = {
            "portal_type": "MaterialType",
            "sort_on": "sortable_title",
            "sort_order": "ascending",
        }

        self.context_actions = {
            _("Add"): {
                "url": "++add++MaterialType",
                "icon": "++resource++bika.lims.images/add.png",
            }
        }

        t = self.context.translate
        self.title = t(_("Material Types"))
        self.description = t(_(""))

        self.show_select_column = True
        self.pagesize = 25

        self.columns = collections.OrderedDict(
            (
                ("title", {"title": _("Title"), "index": "sortable_title"}),
                (
                    "material_class",
                    {"title": _("Material Class")},
                ),
                (
                    "description",
                    {"title": _("Description"), "index": "description"},
                ),
            )
        )

        self.review_states = [
            {
                "id": "default",
                "title": _("Active"),
                "contentFilter": {"is_active": True},
                "columns": self.columns.keys(),
            },
            {
                "id": "inactive",
                "title": _("Inactive"),
                "contentFilter": {"is_active": False},
                "columns": self.columns.keys(),
            },
            {
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

        material_class_list = obj.material_class
        if material_class_list:
            material_class_obj = api.get_object_by_uid(material_class_list[0])
            material_class_title = material_class_obj.title
            material_class_url = material_class_obj.absolute_url()
            material_class_link = get_link(
                material_class_url, material_class_title
            )
            item["material_class"] = material_class_title
            item["replace"]["material_class"] = material_class_link
        return item
