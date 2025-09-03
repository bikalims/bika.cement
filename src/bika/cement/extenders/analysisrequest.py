# -*- coding: utf-8 -*-

from Products.Archetypes.Widget import StringWidget
from Products.Archetypes.Widget import TextAreaWidget
from Products.CMFCore.permissions import View
from archetypes.schemaextender.interfaces import IBrowserLayerAwareExtender
from archetypes.schemaextender.interfaces import ISchemaExtender
from archetypes.schemaextender.interfaces import ISchemaModifier
from zope.component import adapts
from zope.interface import implementer
from zope.interface import implements

from bika.cement.config import _
from bika.cement.interfaces import IBikaCementLayer
from bika.extras.extenders.fields import ExtDateTimeField
from bika.lims.interfaces import IAnalysisRequest
from senaite.core.browser.widgets import DateTimeWidget
from senaite.core.browser.widgets import ReferenceWidget
from senaite.core.catalog import CONTACT_CATALOG
from senaite.core.permissions import FieldEditBatch
from .fields import ExtUIDReferenceField
from .fields import ExtStringField
from .fields import ExtTextField


cast_date_field = ExtDateTimeField(
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

curing_method_field = ExtUIDReferenceField(
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

mix_material_field = ExtUIDReferenceField(
    'MixMaterial',
    required=0,
    allowed_types=('MixMaterial',),
    mode="rw",
    write_permission=FieldEditBatch,
    read_permission=View,
    widget=ReferenceWidget(
        label=_("Mix Material"),
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

supplier_field = ExtUIDReferenceField(
    'Supplier',
    required=0,
    allowed_types=('Supplier',),
    mode="rw",
    write_permission=FieldEditBatch,
    read_permission=View,
    widget=ReferenceWidget(
        label=_("Supplier"),
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

supplier_contact_field = ExtUIDReferenceField(
    'SupplierContact',
    required=0,
    allowed_types=('SupplierContact',),
    mode="rw",
    write_permission=FieldEditBatch,
    read_permission=View,
    widget=ReferenceWidget(
        label=_("Supplier Contact"),
        render_own_label=True,
        visible={
            'add': 'edit',
            'secondary': 'disabled',
        },
        catalog_name=CONTACT_CATALOG,
        base_query={"is_active": True,
                    "sort_on": "sortable_title",
                    "sort_order": "ascending"},
        showOn=True,
    ),
)

supplier_location_field = ExtUIDReferenceField(
    'SupplierLocation',
    required=0,
    allowed_types=('SupplierLocation',),
    mode="rw",
    write_permission=FieldEditBatch,
    read_permission=View,
    widget=ReferenceWidget(
        label=_("Supplier Location"),
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

sample_name_field = ExtStringField(
    'SampleName',
    mode="rw",
    write_permission=FieldEditBatch,
    read_permission=View,
    widget=StringWidget(
        label=_(u"Name"),
        description=_(u""),
        visible={
            'add': 'edit',
            'secondary': 'disabled',
        },
        render_own_label=True,
    ),
)

description_field = ExtTextField(
    "SampleDescription",
    widget=TextAreaWidget(
        label=_("Description"),
        description=_(""),
        visible={
            'add': 'edit',
            'secondary': 'disabled',
        },
        size=10,
        allow_file_upload=False,
        default_mime_type='text/x-rst',
        output_mime_type='text/x-html',
        rows=3,
        render_own_label=True,
    ),
)

lot_number_field = ExtStringField(
    'LotNumber',
    mode="rw",
    write_permission=FieldEditBatch,
    read_permission=View,
    widget=StringWidget(
        label=_(u"Lot Number"),
        description=_(u""),
        visible={
            'add': 'edit',
            'secondary': 'disabled',
        },
        render_own_label=True,
    ),
)



@implementer(ISchemaExtender, IBrowserLayerAwareExtender)
class AnalysisRequestSchemaExtender(object):
    adapts(IAnalysisRequest)
    layer = IBikaCementLayer

    fields = [
        sample_name_field,
        cast_date_field,
        curing_method_field,
        mix_material_field,
        supplier_field,
        supplier_contact_field,
        supplier_location_field,
        description_field,
        lot_number_field,
    ]

    def __init__(self, context):
        self.context = context

    def getOrder(self, schematas):
        return schematas

    def getFields(self):
        return self.fields


class AnalysisRequestSchemaModifier(object):
    adapts(IAnalysisRequest)
    implements(ISchemaModifier)
    layer = IBikaCementLayer

    def __init__(self, context):
        self.context = context

    def fiddle(self, schema):
        """
        """
        schema.moveField('SampleName', after='Contact')
        schema.moveField('SampleDescription', after='SampleName')

        return schema
