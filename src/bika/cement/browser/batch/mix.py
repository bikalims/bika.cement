# -*- coding: utf-8 -*-

import collections
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.contentlisting.interfaces import IContentListing
from plone.app.layout.globals.interfaces import IViewView
from zope.interface import alsoProvides
from zope.interface import implements
from plone.app.layout.viewlets import ViewletBase

from bika.lims import api
from bika.lims.browser import BrowserView
from bika.lims.utils import get_link, get_link_for
from senaite.app.listing import ListingView
from senaite.core.catalog import SETUP_CATALOG

from bika.cement.config import _
from bika.cement.config import is_installed


class BatchMixView(BrowserView):
    implements(IViewView)
    template = ViewPageTemplateFile("templates/mix_view.pt")
    mortar_p_template = ViewPageTemplateFile(
        "templates/mix_mortar_paste_view.pt"
    )

    def __init__(self, context, request):
        super(BatchMixView, self).__init__(context, request)
        alsoProvides(request, IContentListing)

    def __call__(self):
        #
        batch = self.context
        mix_design = batch.get_mix_design()
        if not mix_design:
            return self.template()

        # TODO: check sample view and just render the data regardless of type
        mix_design_type = mix_design.mix_design_type
        if not mix_design_type:
            return self.template()

        portal_type = api.get_object_by_uid(mix_design_type[0]).portal_type
        if not portal_type:
            return self.template()
        if portal_type == "MixDesignConcrete":
            return self.template()
        if portal_type == "MixDesignMortarPaste":
            return self.mortar_p_template()

        return self.template()

    def get_mix_design(self):
        batch = self.context
        return batch.get_mix_design()

    def get_mix_design_concrete(self):
        mix_design = self.get_mix_design()
        if not mix_design:
            return None
        return mix_design.get_mix_design_concrete()

    def get_mix_design_mortar_paste(self):
        mix_design = self.get_mix_design()
        if not mix_design:
            return None
        query = {
            "portal_type": "MixDesignMortarPaste",
            "path": {"query": api.get_path(mix_design), },
        }
        brains = api.search(query, SETUP_CATALOG)
        if len(brains) == 1:
            return api.get_object(brains[0])


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


class MixMaterialTable(ListingView):

    """Displays all available sample containers in a table"""

    def __init__(self, context, request):
        super(MixMaterialTable, self).__init__(context, request)
        self.catalog = SETUP_CATALOG
        self.contentFilter = {
            "UID": self.get_mix_design().mix_materials
            if self.get_mix_design()
            else [],
        }
        t = self.context.translate
        self.title = t(_("Mix Materials"))
        self.icon = api.get_icon("MixMaterials", html_tag=False)
        self.show_search = False
        self.show_workflow_action_buttons = False
        self.show_select_column = False
        self.enable_ajax_transitions = None
        self.columns = collections.OrderedDict((
            ("material_class", {
                "title": _("Class"),
                "index": "sortable_title"}),
            ("material_type", {
                "title": _("Type"),
                "index": "material_type"}),
            ("title", {
                "title": _("Title"),
                "index": "sortable_title"}),
            ("specific_gravity", {
                "title": _("SG"),
                "index": "specific_gravity"}),
            ("absorption_rate", {
                "title": _("Amount"),
                "index": "absorption_rate"}),
        ))

        self.review_states = [
            {
                "id": "default",
                "title": _("Active"),
                "columns": self.columns.keys(),
            }
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
        item["specific_gravity"] = obj.specific_gravity
        item["absorption_rate"] = obj.absorption_rate

        # Material Type
        material_type_list = obj.material_type
        if material_type_list:
            material_type = api.get_object_by_uid(material_type_list[0])
            material_type_title = material_type.title
            material_type_url = material_type.absolute_url()
            material_type_link = get_link(
                material_type_url, material_type_title
            )
            item["material_type"] = material_type_title
            item["replace"]["material_type"] = material_type_link
            m_class = api.get_object_by_uid(material_type.material_class[0])
            item["material_class"] = m_class.title
            item["replace"]["material_class"] = get_link(
                m_class.absolute_url(), m_class.title
            )
        return item

    def get_mix_design(self):
        batch = self.context
        return batch.get_mix_design()
