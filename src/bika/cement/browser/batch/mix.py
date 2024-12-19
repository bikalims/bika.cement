# -*- coding: utf-8 -*-

from Acquisition import aq_base
import openpyxl
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.contentlisting.interfaces import IContentListing
from plone.app.layout.globals.interfaces import IViewView
from zope.interface import alsoProvides
from zope.interface import implements
from plone.app.layout.viewlets import ViewletBase

from bika.lims import api
from bika.lims.browser import BrowserView
from senaite.core.catalog import SETUP_CATALOG

from bika.cement.browser.controlpanel.mixmaterials import (
    MixMaterialsView as MMV,
)
from bika.cement.config import _
from bika.cement.config import is_installed


class BatchMixView(BrowserView):
    implements(IViewView)
    template = ViewPageTemplateFile("templates/mix_view.pt")

    def __init__(self, context, request):
        super(BatchMixView, self).__init__(context, request)
        alsoProvides(request, IContentListing)

    def __call__(self):
        batch = self.context
        mix_template_file = batch.MixTemplateFile
        if not mix_template_file:
            return self.template()
        if self.get_mix_design():  # A mix design already exists
            return self.template()

        blob_file = mix_template_file.blob
        sheet_name = "SSD & Batch values"
        data = self.get_data_from_blob_file(blob_file, sheet_name)
        mix_design_data = self.parse_mix_design_data(data)
        concrete_data = self.parse_mix_design_concrete_data(data)
        mix_design = self.create_mix_design(mix_design_data)
        self.create_concrete_mix_design(mix_design, concrete_data)
        return self.template()

    def get_mix_design(self):
        batch = self.context
        query = {
            "portal_type": "MixDesign",
            "path": {
                "query": api.get_path(batch),
            },
        }
        brains = api.search(query, SETUP_CATALOG)
        if len(brains) == 1:
            return api.get_object(brains[0])

    def get_mix_design_concrete(self):
        mix_design = self.get_mix_design()
        query = {
            "portal_type": "MixDesignConcrete",
            "path": {
                "query": api.get_path(mix_design),
            },
        }
        brains = api.search(query, SETUP_CATALOG)
        if len(brains) == 1:
            return api.get_object(brains[0])

    def get_data_from_blob_file(self, blob, sheet_name=None):
        # Step 1: Open the blob
        base_blob = aq_base(blob)
        with base_blob.open("r") as blob_file:
            blob_file.seek(0)
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
        mix_design_data["title"] = data[0][2]
        mix_design_data["project"] = data[0][2]
        mix_design_data["mix_design_type"] = data[0][4]
        mix_materials = self.parse_mix_materials(data)
        mix_design_data.update({"mix_materials": mix_materials})
        return mix_design_data

    def parse_mix_materials(self, data):
        mix_materials = []
        in_materials_section = False
        for row in data:  # to-do:how to stop going through list
            if in_materials_section and row[1] and row[1] != "Classes":
                material_class = row[1]
                material_type = row[2]
                mix_material = row[3]
                mix_info = [mix_material, material_type, material_class]
                mix_material = self.material_mix_validation(mix_info)
                if mix_material:
                    mix_materials.append(mix_material)
            if "Design and Batch" in row[1]:
                in_materials_section = True
        return mix_materials

    def material_mix_validation(self, mix_data):
        material_type_uid = self.get_material_type_uid(mix_data[1])
        if not material_type_uid:
            return
        material_class_uid = self.get_material_class_uid(
            material_type_uid, mix_data[2]
        )
        if not material_class_uid:
            return
        mix_material_uid = self.get_mix_material_uid(mix_data[1], mix_data[0])
        if not mix_material_uid:
            return
        return mix_material_uid

    def get_material_type_uid(self, material_type):
        setup = self.context.setup
        query = {
            "portal_type": "MaterialType",
            "path": {
                "query": api.get_path(setup.materialtypes),
            },
        }
        brains = api.search(query, SETUP_CATALOG)
        for type_obj in brains:
            if type_obj.Title == material_type:
                return api.get_uid(type_obj)
        return

    def get_material_class_uid(self, material_type_uid, material_class):
        material_type = api.get_object_by_uid(material_type_uid)
        material_class_uid = material_type.material_class
        material_class_obj = api.get_object_by_uid(material_class_uid[0])
        if material_class_obj.Title() == material_class:
            return material_class_uid[0]
        return

    def get_mix_material_uid(self, material_type_title, mix_material):
        setup = self.context.setup
        query = {
            "portal_type": "MixMaterial",
            "path": {
                "query": api.get_path(setup.mixmaterials),
            },
        }
        brains = api.search(query, SETUP_CATALOG)
        for mix_obj_product in brains:
            mix_obj = mix_obj_product.getObject()
            if mix_obj.Title() == mix_material:
                mix_material_type_uid = mix_obj.material_type[0]
                mix_material_type_title = api.get_object_by_uid(
                    mix_material_type_uid
                ).Title()
                if mix_material_type_title == material_type_title:
                    return api.get_uid(mix_obj)
        return

    def parse_mix_design_concrete_data(self, data):
        concrete_data = {}
        concrete_data["title"] = data[0][2]
        concrete_data["batch_volume"] = data[0][6]
        concrete_data["design"] = data[1][2]  # design number
        concrete_data["replacement"] = data[1][4]
        concrete_data["paste_content"] = data[1][6]
        # missing design w/cm
        concrete_data["total_cm"] = data[2][4]
        # missing theoretical volume
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

    def create_mix_design(self, data):
        batch = self.context
        mix_design = api.create(batch, "MixDesign")
        mix_design.title = data.get("title")
        mix_design.project = data.get("project")
        mix_design.mix_design_type = data.get("mix_design_type")
        mix_design.mix_materials = data.get("mix_materials")
        # mix_design.edit(**data)
        return mix_design

    def create_concrete_mix_design(self, mix_design, data):
        concrete_mix_design = api.create(mix_design, "MixDesignConcrete")
        concrete_mix_design.title = data.get("title")
        concrete_mix_design.batch_volume = data.get("batch_volume")
        concrete_mix_design.design = data.get("design")
        concrete_mix_design.replacement = data.get("replacement")
        concrete_mix_design.paste_content = data.get("paste_content")
        concrete_mix_design.total_cm = data.get("total_cm")
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
        return concrete_mix_design


class MixMaterialViewlet(ViewletBase):
    """Laboratory analyses section viewlet for Sample view"""

    index = ViewPageTemplateFile("templates/mixmaterials.pt")

    title = _("Materials")
    icon_name = "analysisservice"
    capture = "lab"

    @property
    def batch(self):
        return self.context

    def is_collapsed(self):
        return False

    def available(self):
        """Returns true if this sample contains at least one analysis for the
        point of capture (capture)
        """
        return True

    def get_listing_view(self):
        request = api.get_request()
        view_name = "table_mix_material"
        view = api.get_view(view_name, context=self.batch, request=request)
        return view

    def contents_table(self):
        view = self.get_listing_view()
        view.update()
        view.before_render()
        return view.ajax_contents_table()


class MixMaterialTable(MMV):
    """Displays all available sample containers in a table"""

    def __init__(self, context, request):
        super(MixMaterialTable, self).__init__(context, request)
        self.contentFilter = {
            "UID": self.get_mix_design().mix_materials,
        }
        self.show_search = False
        self.show_workflow_action_buttons = False
        self.show_select_column = False
        self.enable_ajax_transitions = None

    def before_render(self):
        if not is_installed():
            return

        # Remove review states, show all(default) and no filter
        for i in range(len(self.review_states)):
            if self.review_states[i]["id"] != "default":
                continue
            self.review_states = [self.review_states[i]]
            break

    def get_mix_design(self):
        batch = self.context
        query = {
            "portal_type": "MixDesign",
            "path": {
                "query": api.get_path(batch),
            },
        }
        brains = api.search(query, SETUP_CATALOG)
        if len(brains) == 1:
            return api.get_object(brains[0])

        values = batch.values()
        mix_design = [md for md in values if md.portal_type == "MixDesign"]
        if len(mix_design) == 1:
            return mix_design[0]
