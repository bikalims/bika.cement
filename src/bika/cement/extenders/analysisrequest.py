# -*- coding: utf-8 -*-

from archetypes.schemaextender.interfaces import IBrowserLayerAwareExtender
from archetypes.schemaextender.interfaces import ISchemaExtender
from zope.component import adapts
from zope.interface import implementer

from bika.extras.extenders.fields import ExtDateTimeField
from bika.lims.interfaces import IAnalysisRequest
from bika.cement.config import _
from bika.cement.interfaces import IBikaCementLayer
from senaite.core.browser.widgets import DateTimeWidget


cast_date = ExtDateTimeField(
    "CastDate",
    widget=DateTimeWidget(
        label=_("Cast Date"),
        description=_("Cast Date"),
        show_time=True,
        visible={
            "add": "edit",
        },
        mode="rw",
        render_own_label=True,
    ),
)


@implementer(ISchemaExtender, IBrowserLayerAwareExtender)
class AnalysisRequestSchemaExtender(object):
    adapts(IAnalysisRequest)
    layer = IBikaCementLayer

    fields = [
        cast_date,
    ]

    def __init__(self, context):
        self.context = context

    def getOrder(self, schematas):
        return schematas

    def getFields(self):
        return self.fields
