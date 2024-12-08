# -*- coding: utf-8 -*-

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.contentlisting.interfaces import IContentListing
from plone.app.layout.globals.interfaces import IViewView
from zope.interface import alsoProvides
from zope.interface import implements

from bika.lims.browser import BrowserView


class BatchMixView(BrowserView):
    implements(IViewView)
    template = ViewPageTemplateFile("templates/mix_view.pt")

    def __init__(self, context, request):
        super(BatchMixView, self).__init__(context, request)
        alsoProvides(request, IContentListing)

    def __call__(self):
        return self.template()
