# -*- coding: utf-8 -*-

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
    mortar_p_template = ViewPageTemplateFile("templates/mix_morta_paste_view.pt")

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
            "path": {
                "query": api.get_path(mix_design),
            },
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


class MixMaterialTable(MMV):
    """Displays all available sample containers in a table"""

    def __init__(self, context, request):
        super(MixMaterialTable, self).__init__(context, request)
        self.contentFilter = {
            "UID": self.get_mix_design().mix_materials if self.get_mix_design() else [],
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
        return batch.get_mix_design()
