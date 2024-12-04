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
from Products.CMFCore.permissions import View
from bika.lims.permissions import FieldEditBatch
from senaite.core.browser.widgets import ReferenceWidget
from .fields import ExtUIDReferenceField


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

curing_method = ExtUIDReferenceField(
    'CuringMethod',
    required=0,
    allowed_types=('CuringMethod',),
    mode="rw",
    write_permission=FieldEditBatch,
    read_permission=View,
    widget=ReferenceWidget(
        label=_("Curing Method"),
        render_own_label=True,
        visible={
            'add': 'edit',
            'secondary': 'disabled',
        },
        catalog_name='senaite_catalog_setup',
        base_query={"is_active": True,
                    "sort_on": "sortable_title",
                    "sort_order": "ascending"},
        showOn=True,
    ),
)


@implementer(ISchemaExtender, IBrowserLayerAwareExtender)
class AnalysisRequestSchemaExtender(object):
    adapts(IAnalysisRequest)
    layer = IBikaCementLayer

    fields = [
        cast_date,
        curing_method,
    ]

    def __init__(self, context):
        self.context = context

    def getOrder(self, schematas):
        return schematas

    def getFields(self):
        return self.fields
