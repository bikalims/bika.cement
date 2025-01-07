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

import io
import six
import openpyxl
from archetypes.schemaextender.interfaces import IExtensionField
from openpyxl import load_workbook
from plone.app.blob.field import FileField
from Products.Archetypes import public
from zope.interface import implements
from zope.site.hooks import getSite

from bika.lims import api
from bika.lims.browser.fields import UIDReferenceField


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
            change_samples = self.has_spreadsheet_file_content_changed(
                batch, "MixSpreadsheet")
            self.set(batch, value)
            sheet_name = "SSD & Batch values"
            if batch.MixSpreadsheet:
                blob = batch.MixSpreadsheet.blob
                data = self.get_data_from_blob_file(blob, sheet_name)
                mix_design_data = self.parse_mix_design_data(data)
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

    def has_spreadsheet_file_content_changed(self, obj, field_name):
        field = obj.getField(field_name)
        if not field:
            msg = "Field '{}' is not a valid file field.".format(field_name)
            raise ValueError(msg)

        current_file = field.get(obj)
        if not current_file:
            return False

        original_files = getattr(obj, '_at_field_original_value', {})
        original_file = original_files.get(field_name, None)
        if not original_file:
            return True

        # Compare spreadsheet content
        current_content = load_workbook(io.BytesIO(current_file.data))
        original_content = load_workbook(io.BytesIO(original_file.data))

        return not self.compare_workbooks(current_content, original_content)

    def compare_workbooks(self, wb1, wb2):
        """Simple comparison of two workbooks."""
        if len(wb1.sheetnames) != len(wb2.sheetnames):
            return False

        for sheet1, sheet2 in zip(wb1, wb2):
            if sheet1.title != sheet2.title:
                return False
            if list(sheet1.values) != list(sheet2.values):
                return False

        return True

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
        # to-do: (mix_materials)
        return mix_design_data

    def parse_mix_design_concrete_data(self, data):
        concrete_data = {}
        concrete_data["batch_volume"] = data[0][6]
        concrete_data["design_title"] = data[1][2]  # design w/cm (title)
        concrete_data["replacement"] = data[1][4]
        concrete_data["paste_content"] = data[1][6]
        concrete_data["total_cm"] = data[2][4]
        concrete_data["theoretical_volume"] = data[2][6]
        concrete_data["super_air_meter"] = data[2][8]
        concrete_data["design_air"] = data[3][2]
        concrete_data["design_slump"] = data[3][4]
        concrete_data["theoretical_unit_weight"] = data[3][6]
        concrete_data["measured_air"] = data[4][2]
        concrete_data["measured_slump"] = data[4][4]
        # date missing
        concrete_data["lab_temperature"] = data[5][4]
        # missing time
        concrete_data["concrete_temp"] = data[6][4]
        return concrete_data

    def create_mix_design(self, batch, data):
        mix_design = api.create(batch, "MixDesign")
        mix_design.title = data.get("design_title")
        mix_design.project = data.get("project")
        # mix_design.mix_design_type = data.get("mix_design_type")
        # mix_design.edit(**data)
        return mix_design

    def create_concrete_mix_design(self, mix_design, data):
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
        # concrete_mix_design.edit(**data)
        mix_design.mix_design_type = [concrete_mix_design.UID()]
        return concrete_mix_design

    def mix_materials(self, mix_design, data):
        setup = api.get_senaite_setup()
        folder = setup.get("mixmaterials")
        mix_mat_data = data[9:]
        mix_materials = []
        for mx in mix_mat_data:
            # m_class = mx[1]
            # m_type = mx[2]
            m_name = mx[3]
            # TODO: Check if MixMaterial already exists
            mix_material = api.create(folder, "MixMaterial", title=m_name)
            mix_materials.append(mix_material.UID())
        mix_design.mix_materials = mix_materials


class ExtMixSpreadsheetFileField(MixSpreadsheetFileExtensionField, FileField):
    "Field extender"
