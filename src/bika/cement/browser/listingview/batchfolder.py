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
# Copyright 2018-2021 by it's authors.
# Some rights reserved, see README and LICENSE.

from bika.cement.config import _
from bika.cement.config import is_installed
from bika.lims.utils import get_link
from bika.lims import api
from senaite.app.listing.interfaces import IListingView
from senaite.app.listing.interfaces import IListingViewAdapter
from zope.component import adapts
from zope.interface import implements


class BatchesListingViewAdapter(object):
    adapts(IListingView)
    implements(IListingViewAdapter)

    def __init__(self, listing, context):
        self.listing = listing
        self.context = context

    def before_render(self):
        if not is_installed():
            return

        mix_template_file = [
            (
                "MixSpreadsheet",
                {
                    "toggle": False,
                    "sortable": False,
                    "title": _("Mix Spreadsheet"),
                },
            )
        ]

        self.listing.columns.update(mix_template_file)
        for i in range(len(self.listing.review_states)):
            self.listing.review_states[i]["columns"].append("MixSpreadsheet")

    def folder_item(self, obj, item, index):
        if not is_installed():
            return item
        obj = api.get_object(obj)
        if not hasattr(obj, "MixSpreadsheet"):
            return item
        # using the regular obj.DateExported gives us errors
        # hence we are using the schema to get the value
        mix_template_file = obj.MixSpreadsheet
        filesize = mix_template_file.get_size()
        if filesize > 0:
            url = item.get("url")
            filename = mix_template_file.getFilename()
            download_url = "{}/at_download/MixSpreadsheet".format(url)
            anchor = get_link(download_url, filename)
            item["MixSpreadsheet"] = filename
            item["replace"]["MixSpreadsheet"] = anchor
        return item
