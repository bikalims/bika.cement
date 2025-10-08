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
# Copyright 2018-2025 by it's authors.
# Some rights reserved, see README and LICENSE.

from bika.lims import api
from bika.lims import logger
from senaite.core.catalog import SETUP_CATALOG
from senaite.core.exportimport.setupdata import WorksheetImporter as WI


class WorksheetImporter(WI):
    def safe_float(self, value):
        """Convert a spreadsheet value to a float or None safely."""
        if value in (None, "", " "):
            return None
        try:
            f = float(value)
        except (ValueError, TypeError):
            return None
        return f


class Brands(WorksheetImporter):

    def Import(self):
        sc = api.get_tool(SETUP_CATALOG)
        container = self.context.setup.brands
        for row in self.get_rows(3):
            title = row.get("title")
            if not title:
                continue
            obj = self.get_object(sc, "Brand", title=title)
            if obj:
                continue
            api.create(container, "Brand",
                       title=title, description=row.get("description"))


class Material_Classes(WorksheetImporter):

    def Import(self):
        # Refer to the default folder
        container = self.context.setup.materialclasses
        sc = api.get_tool(SETUP_CATALOG)
        # Iterate through the rows
        for row in self.get_rows(3):
            title = row.get("title")
            if not title:
                continue
            obj = self.get_object(sc, "MaterialClass", title=title)
            if obj:
                continue
            sortKey = float(row.get("SortKey")) if row.get("SortKey") else 0.0
            api.create(container, "MaterialClass",
                       title=title, description=row.get("description"),
                       sort_key=sortKey)


class Mix_Types(WorksheetImporter):

    def Import(self):
        sc = api.get_tool(SETUP_CATALOG)
        container = self.context.setup.mixtypes
        for row in self.get_rows(3):
            title = row.get("title")
            if not title:
                continue
            m_type = self.get_object(sc, "MixType", title=title)
            if m_type:
                continue

            api.create(container, "MixType",
                       title=title, description=row.get("description"))


class Material_Types(WorksheetImporter):

    def Import(self):
        container = self.context.setup.materialtypes
        sc = api.get_tool(SETUP_CATALOG)
        for row in self.get_rows(3):
            title = row.get("title")
            if not title:
                msg = "Error in in {}. Missing Title field."
                logger.warning(msg.format(self.sheetname))
                continue
            m_type = self.get_object(sc, "MaterialType", title=title)
            if m_type:
                continue

            class_title = row.get("Class_title", None)
            if not class_title:
                msg = "Error in {}. Material Class field missing.mk"
                logger.warning(msg.format(self.sheetname))
                continue

            m_class = self.get_object(sc, "MaterialClass", title=class_title)
            if not m_class:
                msg = "Error in {}. Material Class '{}' is wrong."
                logger.warning(msg.format(self.sheetname, class_title))
                continue

            description = row.get("description", "")
            api.create(container, "MaterialType",
                       title=title,
                       description=description,
                       material_class=[m_class.UID()])


class Materials(WorksheetImporter):

    def Import(self):
        container = self.context.setup.mixmaterials
        sc = api.get_tool(SETUP_CATALOG)
        for row in self.get_rows(3):
            title = row.get("title")
            if not title:
                msg = "Error in in {}. Missing Title field."
                logger.warning(msg.format(self.sheetname))
                continue

            m_mat = self.get_object(sc, "MixMaterial", title=title)
            if m_mat:
                continue

            # Material Type
            mt_title = row.get("MaterialType_title", None)
            if not mt_title:
                msg = "Error in {}. Material Class field missing."
                logger.warning(msg.format(self.sheetname))
                mt = []
            else:
                mt = self.get_object(sc, "MaterialType", title=mt_title)
            if not mt:
                msg = "Error in {}. Material Class '{}' is wrong."
                logger.warning(msg.format(self.sheetname, mt_title))

            # Brand
            b_title = row.get("Brand_title", None)
            if not b_title:
                msg = "Error in {}. Material Class field missing."
                logger.warning(msg.format(self.sheetname))
                brand = []

            else:
                brand = self.get_object(sc, "Brand", title=b_title)

            if not brand:
                msg = "Error in {}. Brand '{}' is wrong."
                logger.warning(msg.format(self.sheetname, b_title))

            # Manufacturer
            m_title = row.get("Manufacturer_title", None)
            if not m_title:
                msg = "Error in {}. Manufacturer field missing."
                logger.warning(msg.format(self.sheetname))
                manuf = []

            else:
                manuf = self.get_object(sc, "Manufacturer", title=m_title)

            if not manuf:
                msg = "Error in {}. Manufacturer '{}' is wrong."
                logger.warning(msg.format(self.sheetname, b_title))

            # Supplier
            s_title = row.get("Supplier_title", None)
            if not s_title:
                msg = "Error in {}. Supplier field missing."
                logger.warning(msg.format(self.sheetname))
                supplier = []

            else:
                supplier = self.get_object(sc, "Supplier", title=s_title)

            if not supplier:
                msg = "Error in {}. Supplier '{}' is wrong."
                logger.warning(msg.format(self.sheetname, b_title))

            # Manufacturer
            m_title = row.get("Manufacturer_title", None)
            if not m_title:
                msg = "Error in {}. Manufacturer field missing."
                logger.warning(msg.format(self.sheetname))
                manuf = []

            else:
                manuf = self.get_object(sc, "Manufacturer", title=m_title)

            if not manuf:
                msg = "Error in {}. Manufacturer '{}' is wrong."
                logger.warning(msg.format(self.sheetname, b_title))

            description = row.get("description", "")
            specific_gravity = self.safe_float(row.get("Specific_Gravity"))
            absorption_rate = self.safe_float(row.get("Absorption_Rate"))

            api.create(container, "MixMaterial",
                       title=title,
                       description=description,
                       specific_gravity=specific_gravity,
                       absorption_rate=absorption_rate,
                       material_type=[mt.UID()] if mt else [],
                       brand=[brand.UID()] if brand else [],
                       supplier=[supplier.UID()] if supplier else [],
                       manufacturer=[manuf.UID()] if manuf else [],
                       )
