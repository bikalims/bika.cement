# -*- coding: utf-8 -*-

from AccessControl import ClassSecurityInfo
from plone.autoform import directives
from plone.dexterity.content import Container
from plone.supermodel import model
from zope import schema
from zope.interface import implementer

from bika.lims import api
from bika.lims.interfaces import IDeactivable
from senaite.core.catalog import SETUP_CATALOG
from senaite.core.schema import DatetimeField
from senaite.core.schema import UIDReferenceField
from senaite.core.z3cform.widgets.datetimewidget import DatetimeWidget

from bika.cement.config import _
from bika.cement.interfaces import IMixDesign


class IMixDesignSchema(model.Schema):
    """Marker interface and Dexterity Python Schema for Curing Methods"""

    title = schema.TextLine(
        title=_(u"title_mix_design_title", default=u"Mix Design"),
        required=True,
    )
    description = schema.Text(
        title=_(u"title_mix_design_description", default=u"Description"),
        required=False,
    )
    project = schema.TextLine(
        title=_(u"title_mix_design_project", default=u"Project"),
        required=True,
    )
    mix_design_type = UIDReferenceField(
        title=_(u"title_mix_design_type", default=u"Mix Design Type"),
        relationship="MixDesignTypes",
        allowed_types=("MixDesignConcrete", "MixDesignMortarPaste"),
        multi_valued=False,
        required=False,
    )
    mix_materials = UIDReferenceField(
        title=_(u"title_mix_design_mix_material", default=u"Mix Materials"),
        relationship="MixDesignMixMaterial",
        allowed_types=("MixMaterial", ),
        multi_valued=True,
        required=False,
    )

    directives.widget("date", DatetimeWidget, show_time=False)
    date = DatetimeField(
        title=_(u"label_mix_design_date", default=u"Date"),
        description=_(
            u"description_mix_design_date",
            default=u"Mix Design Date"),
        required=False,
    )
    additional_info = schema.Text(
        title=_(u"title_mix_design_addtional_info", default=u"Additional Info"),
        required=False,
    )


@implementer(IMixDesign, IMixDesignSchema, IDeactivable)
class MixDesign(Container):
    """Content-type class for IMixDesign"""

    _catalogs = [SETUP_CATALOG]

    security = ClassSecurityInfo()

    @security.private
    def accessor(self, fieldname):
        """Return the field accessor for the fieldname"""
        schema = api.get_schema(self)
        if fieldname not in schema:
            return None
        return schema[fieldname].get

    @security.private
    def mutator(self, fieldname):
        """Return the field mutator for the fieldname"""
        schema = api.get_schema(self)
        if fieldname not in schema:
            return None
        result = schema[fieldname].set
        self.reindexObject()
        return result
