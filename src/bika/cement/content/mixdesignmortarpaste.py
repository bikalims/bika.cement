# -*- coding: utf-8 -*-

from AccessControl import ClassSecurityInfo
from plone.dexterity.content import Container
from plone.supermodel import model
from zope import schema
from zope.interface import implementer

from bika.lims import api
from bika.lims.interfaces import IDeactivable
from senaite.core.catalog import SETUP_CATALOG

from bika.cement.config import _
from bika.cement.interfaces import IMixDesignMortarPaste


class IMixDesignMortarPasteSchema(model.Schema):
    """Marker interface and Dexterity Python Schema for Curing Methods"""

    title = schema.TextLine(
        title=_(
            u"title_mix_design_mortar_paste_title",
            default=u"Title"),
        required=True,
    )

    description = schema.Text(
        title=_(
            u"title_mix_design_mortar_paste_description",
            default=u"Description"),
        required=False,
    )
    design = schema.Float(
        title=_(
            u"title_mix_design_mortar_paste_design",
            default=u"Design W/CM"),
        required=False,
    )
    lab_temperature = schema.Float(
        title=_(
            u"title_mix_design_mortar_paste_lab_temperature",
            default=u"Lab Temperature"),
        description=_(
            u"description_mix_design_mortar_paste_lab_temperature",
            default=u"Unit used is Fahrenheit (°F)"),
        required=False,
    )
    mold_numbers = schema.Float(
        title=_(
            u"title_mix_design_mortar_paste_mould_numbers",
            default=u"Mold Numbers"),
        description=_(
            u"description_mix_design_mortar_paste_mould_numbers",
            default=u""),
        required=False,
    )
    replacement = schema.Float(
        title=_(
            u"title_mix_design_mortar_paste_replacement",
            default=u"Replacement"),
        description=_(
            u"description_mix_design_mortar_paste_replacement",
            default=u"Unit used is Percentage (%)"),
        required=False,
    )
    mortar_temperature = schema.Float(
        title=_(
            u"title_mix_design_mortar_paste_mortar_temperature",
            default=u"Mortar Temperature"),
        description=_(
            u"description_mix_design_mortar_paste_mortar_temperature",
            default=u"Unit used is Fahrenheit (°F)"),
        required=False,
    )
    mortar_flow = schema.Text(
        title=_(
            u"title_mix_design_mortar_paste_mortar_flow",
            default=u"Mortar Flow"),
        required=False,
    )


@implementer(IMixDesignMortarPaste, IMixDesignMortarPasteSchema, IDeactivable)
class MixDesignMortarPaste(Container):
    """Content-type class for IMixDesignMortarPaste"""

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
