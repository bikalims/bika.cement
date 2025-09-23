# -*- coding: utf-8 -*-

from archetypes.schemaextender.interfaces import IBrowserLayerAwareExtender
from archetypes.schemaextender.interfaces import ISchemaExtender
from bika.concrete.config import _
from bika.concrete.interfaces import IBikaCementLayer
from bika.concrete.extenders.fields import ExtMixSpreadsheetFileField
from bika.lims.interfaces import IBatch
from Products.Archetypes.atapi import FileWidget
from zope.component import adapts
from zope.interface import implementer


mix_template_file = ExtMixSpreadsheetFileField(
    "MixSpreadsheet",
    widget=FileWidget(
        label=_("Mix Spreadsheet"),
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
