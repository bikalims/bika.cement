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

import six
import openpyxl
from archetypes.schemaextender.interfaces import IExtensionField
from plone.app.blob.field import FileField
from Products.Archetypes import public
from zope.interface import implements
from zope.site.hooks import getSite

from bika.lims import api
from bika.lims.browser.fields import UIDReferenceField
from senaite.core.catalog import SETUP_CATALOG
from bika.cement.utils import format_number


class ExtensionField(object):
    """Mix-in class to make Archetypes fields not depend on generated
    accessors and mutators, and use AnnotationStorage by default.
    """

    implements(IExtensionField)
    storage = public.AnnotationStorage()

    def __init__(self, *args, **kwargs):
        super(ExtensionField, self).__init__(*args, **kwargs)
        self.args = args
        self.kwargs = kwargs

    def getAccessor(self, instance):
        def accessor():
            if self.getType().endswith("ReferenceField"):
                return self.get(instance.__of__(getSite()))
            else:
                return self.get(instance)

        return accessor

    def getEditAccessor(self, instance):
        def edit_accessor():
            if self.getType().endswith("ReferenceField"):
                return self.getRaw(instance.__of__(getSite()))
            else:
                return self.getRaw(instance)

        return edit_accessor

    def getMutator(self, instance):
        def mutator(value, **kw):
            if self.getType().endswith("ReferenceField"):
                self.set(instance.__of__(getSite()), value)
            else:
                self.set(instance, value)

        return mutator

    def getIndexAccessor(self, instance):
        name = getattr(self, "index_method", None)
        if name is None or name == "_at_accessor":
            return self.getAccessor(instance)
        elif name == "_at_edit_accessor":
            return self.getEditAccessor(instance)
        elif not isinstance(name, six.string_types):
            raise ValueError("Bad index accessor value: %r", name)
        else:
            return getattr(instance, name)


class ExtUIDReferenceField(ExtensionField, UIDReferenceField):
    "Field extender"


class ExtFileField(ExtensionField, FileField):
    "Field extender"


class MixSpreadsheetFileExtensionField(object):
    """Mix-in class to make Archetypes fields not depend on generated
    accessors and mutators, and use AnnotationStorage by default.
    """

    implements(IExtensionField)
    storage = public.AnnotationStorage()

    def __init__(self, *args, **kwargs):
        super(MixSpreadsheetFileExtensionField, self).__init__(*args, **kwargs)
        self.args = args
        self.kwargs = kwargs

    def getAccessor(self, instance):
        def accessor():
            return self.get(instance)

        return accessor

    def getEditAccessor(self, instance):
        def edit_accessor():
            return self.getRaw(instance)

        return edit_accessor

    def getMutator(self, batch):
        def mutator(value, **kw):
            self.set(batch, value)
            sheet_name = "SSD & Batch values"
            if batch.MixSpreadsheet:
                blob = batch.MixSpreadsheet.blob
                data = self.get_data_from_blob_file(blob, sheet_name)
                mix_design_data = self.parse_mix_design_data(data)
                if not mix_design_data:
                    pu = api.get_tool("plone_utils")
                    msg = "Spreadsheet Mix Design and Project are Required"
                    pu.addPortalMessage(msg, "error")
                    return mutator

                concrete_data = self.parse_mix_design_concrete_data(data)
                mix_design = self.create_mix_design(batch, mix_design_data)
                self.create_concrete_mix_design(mix_design, concrete_data)
                self.mix_materials(mix_design, data)

        return mutator

    def getIndexAccessor(self, instance):
        name = getattr(self, "index_method", None)
        if name is None or name == "_at_accessor":
            return self.getAccessor(instance)
        elif name == "_at_edit_accessor":
            return self.getEditAccessor(instance)
        elif not isinstance(name, six.string_types):
            raise ValueError("Bad index accessor value: %r", name)
        else:
            return getattr(instance, name)

    def get_data_from_blob_file(self, blob, sheet_name=None):
        # Step 1: Open the blob
        with blob.open("r") as blob_file:
            workbook = openpyxl.load_workbook(
                blob_file, data_only=True, read_only=True
            )

            # Step 2: Get the specific sheet
            if sheet_name:
                sheet = workbook[sheet_name]  # Access by name
            else:
                sheet = workbook.active  # Default to the first sheet

            # Step 3: Extract data
            data = []
            coa = False
            for row in sheet.iter_rows(values_only=True):
                if coa and any(row):
                    data.append(row)
                if row:
                    if row[0] == "COA":
                        coa = True
            return data

    def parse_mix_design_data(self, data):
        mix_design_data = {}
        mix_design_data["design_title"] = data[1][2]
        mix_design_data["project"] = data[0][2]
        if not mix_design_data["design_title"]:
            return {}
        if not mix_design_data["project"]:
            return {}

        mix_design_data["additional_info"] = data[0][7]
        date = data[5][2]
        time = data[6][2]
        datetime = date
        if date and time:
            datetime = date.replace(hour=time.hour,
                                    minute=time.minute,
                                    second=time.second,
                                    microsecond=time.microsecond
                    )
        mix_design_data["date"] = datetime
        # to-do: (mix_materials)
        return mix_design_data

    def parse_mix_design_concrete_data(self, data):
        concrete_data = {}
        concrete_data["batch_volume"] = format_number(data[0][6])
        concrete_data["design_title"] = data[1][2]  # design w/cm (title)
        concrete_data["replacement"] = format_number(data[1][4])
        concrete_data["paste_content"] = format_number(data[1][6])
        concrete_data["total_cm"] = format_number(data[2][4])
        concrete_data["theoretical_volume"] = format_number(data[2][6])
        concrete_data["super_air_meter"] = data[2][8]
        concrete_data["design_air"] = format_number(data[3][2])
        concrete_data["design_slump"] = format_number(data[3][4])
        concrete_data["theoretical_unit_weight"] = format_number(data[3][6])
        concrete_data["measured_air"] = format_number(data[4][2])
        concrete_data["measured_slump"] = format_number(data[4][4])
        import pdb; pdb.set_trace()
        concrete_data["lab_temperature"] = format_number(data[5][4])
        concrete_data["concrete_temp"] = format_number(data[6][4])
        # Additional Table
        concrete_data["trucked_volume"] = format_number(data[3][8])
        concrete_data["trucked_number"] = data[4][8]
        concrete_data["ticket_number"] = data[5][8]
        concrete_data["plant_number"] = data[6][8]
        return concrete_data

    def create_mix_design(self, batch, data):
        # NOTE: Only one mix design per batch, or edit the existing mix design
        mix_design = batch.get_mix_design()
        if not mix_design:
            mix_design = api.create(batch, "MixDesign")
        mix_design.title = data.get("design_title")
        mix_design.project = data.get("project")
        mix_design.additional_info = data.get("additional_info")
        mix_design.date = data.get("date")

        # mix_design.mix_design_type = data.get("mix_design_type")
        # mix_design.edit(**data)
        return mix_design

    def create_concrete_mix_design(self, mix_design, data):
        # NOTE: Only one concrete mix per mix design, or edit the existing
        # concrete mix
        concrete_mix_design = mix_design.get_mix_design_concrete()
        if not concrete_mix_design:
            concrete_mix_design = api.create(mix_design, "MixDesignConcrete")
        concrete_mix_design.title = data.get("title")
        concrete_mix_design.batch_volume = data.get("batch_volume")
        concrete_mix_design.design = data.get("design_title")
        concrete_mix_design.replacement = data.get("replacement")
        concrete_mix_design.paste_content = data.get("paste_content")
        concrete_mix_design.total_cm = data.get("total_cm")
        concrete_mix_design.theoretical_volume = data.get("theoretical_volume")
        concrete_mix_design.super_air_meter = data.get("super_air_meter")
        concrete_mix_design.design_air = data.get("design_air")
        concrete_mix_design.design_slump = data.get("design_slump")
        concrete_mix_design.theoretical_unit_weight = data.get(
            "theoretical_unit_weight"
        )
        concrete_mix_design.measured_air = data.get("measured_air")
        concrete_mix_design.measured_slump = data.get("measured_slump")
        concrete_mix_design.lab_temperature = data.get("lab_temperature")
        concrete_mix_design.concrete_temp = data.get("concrete_temp")

        concrete_mix_design.trucked_volume = data.get("trucked_volume")
        concrete_mix_design.trucked_number = data.get("trucked_number")
        concrete_mix_design.ticket_number = data.get("ticket_number")
        concrete_mix_design.plant_number = data.get("plant_number")
        # concrete_mix_design.edit(**data)
        mix_design.mix_design_type = [concrete_mix_design.UID()]
        return concrete_mix_design

    def mix_materials(self, mix_design, data):
        setup = api.get_senaite_setup()
        folder = setup.get("mixmaterials")
        mix_mat_data = data[9:]
        mix_materials = []
        errors = []
        query = {
            "portal_type": "MixMaterial",
            "path": {
                "query": api.get_path(folder),
            },
        }
        for mx in mix_mat_data:
            m_name = mx[3]
            query["title"] = m_name
            # TODO: filter by title once the title index has been added
            brains = api.search(query, SETUP_CATALOG)
            brains = [md for md in brains if md.title == m_name]
            if not brains:
                errors.append(m_name)
                continue
            mix_materials.append(brains[0].UID)
        mix_design.mix_materials = mix_materials
        if errors:
            msg = "Spreadsheet Mix Materials not found: %s" % ", ".join(errors)
            pu = api.get_tool("plone_utils")
            pu.addPortalMessage(msg, "error")


class ExtMixSpreadsheetFileField(MixSpreadsheetFileExtensionField, FileField):
    "Field extender"
