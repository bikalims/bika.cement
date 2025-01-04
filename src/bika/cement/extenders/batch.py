# -*- coding: utf-8 -*-

from archetypes.schemaextender.interfaces import IBrowserLayerAwareExtender
from archetypes.schemaextender.interfaces import ISchemaExtender
from bika.cement.config import _
from bika.cement.interfaces import IBikaCementLayer
from bika.cement.extenders.fields import ExtMixTemplateFileField
from bika.lims.interfaces import IBatch
from Products.Archetypes.atapi import FileWidget
from zope.component import adapts
from zope.interface import implementer


mix_template_file = ExtMixTemplateFileField(
    "MixTemplateFile",
    widget=FileWidget(
        label=_("Mix Template"),
    ),
)


@implementer(ISchemaExtender, IBrowserLayerAwareExtender)
class BatchSchemaExtender(object):
    adapts(IBatch)
    layer = IBikaCementLayer

    fields = [
        mix_template_file,
    ]

    def __init__(self, context):
        self.context = context

    def getOrder(self, schematas):
        return schematas

    def getFields(self):
        return self.fields
