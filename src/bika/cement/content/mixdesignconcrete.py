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
from bika.cement.interfaces import IMixDesignConcrete


class IMixDesignConcreteSchema(model.Schema):
    """Marker interface and Dexterity Python Schema for Curing Methods"""

    title = schema.TextLine(
        title=_(
            u"title_mix_design_concrete_title",
            default=u"Title"),
        required=True,
    )

    description = schema.Text(
        title=_(
            u"title_mix_design_concrete_description",
            default=u"Description"),
        required=False,
    )
    design = schema.Float(
        title=_(
            u"title_mix_design_concrete_design",
            default=u"Design W/CM"),
        required=False,
    )
    theoretical_volume = schema.Float(
        title=_(
            u"title_mix_design_concrete_theorical_volume",
            default=u"Theoretical Volume"),
        description=_(
            u"description_mix_design_concrete_theorical_volume",
            default=u"Unit used is Cubic Feet (cu ft)"),
        required=False,
    )
    design_air = schema.Float(
        title=_(
            u"title_mix_design_concrete_design_air",
            default=u"Design Air"),
        description=_(
            u"description_mix_design_concrete_design_air",
            default=u"Unit used is Percentage (%)"),
        required=False,
    )
    theoretical_unit_weight = schema.Float(
        title=_(
            u"title_mix_design_concrete_theoretical_unit_weight",
            default=u"Theoretical Unit Weight"),
        description=_(
            u"description_mix_design_concrete_theoretical_unit_weight",
            default=u"Unit used is Pound per Cubic Feet (lb/cu ft)"),
        required=False,
    )
    lab_temperature = schema.Float(
        title=_(
            u"title_mix_design_concrete_lab_temperature",
            default=u"Lab Temperature"),
        description=_(
            u"description_mix_design_concrete_concrete_temp",
            default=u"Unit used is Fahrenheit (°F)"),
        required=False,
    )
    design_slump = schema.Float(
        title=_(
            u"title_mix_design_concrete_design_slump",
            default=u"Design Slump (in)"),
        description=_(
            u"description_mix_design_concrete_design_slump",
            default=u"Unit used is (in)"),
        required=False,
    )
    total_cm = schema.Float(
        title=_(
            u"title_mix_design_concrete_total_cm",
            default=u"Total CM"),
        description=_(
            u"description_mix_design_concrete_total_cm",
            default=u"Unit used is Pound (lb)"),
        required=False,
    )
    batch_volume = schema.Float(
        title=_(
            u"title_mix_design_concrete_batch_volume",
            default=u"Batch Volume"),
        description=_(
            u"description_mix_design_concrete_batch_volume",
            default=u"Unit used is Cubic Feet (cu ft)"),
        required=False,
    )
    measured_air = schema.Float(
        title=_(
            u"title_mix_design_concrete_measured_air",
            default=u"Measured Air"),
        description=_(
            u"description_mix_design_concrete_measured_air",
            default=u"Unit used is Percentage (%)"),
        required=False,
    )
    measured_unit_weight = schema.Float(
        title=_(
            u"title_mix_design_concrete_measured_unit_weight",
            default=u"Measured Unit Weight"),
        description=_(
            u"description_mix_design_concrete_measured_unit_weight",
            default=u"Unit used is Pound per Cubic Feet (lb/cu ft)"),
        required=False,
    )
    concrete_temp = schema.Float(
        title=_(
            u"title_mix_design_concrete_concret_temp",
            default=u"Concrete Temp"),
        description=_(
            u"description_mix_design_concrete_concrete_temp",
            default=u"Unit used is Fahrenheit (°F)"),
        required=False,
    )
    measured_slump = schema.Float(
        title=_(
            u"title_mix_design_concrete_measured_slump",
            default=u"Measured Slump (in)"),
        required=False,
    )
    replacement = schema.Float(
        title=_(
            u"title_mix_design_concrete_replacement",
            default=u"Replacement"),
        description=_(
            u"description_mix_design_concrete_replacement",
            default=u"Unit used is Percentage (%)"),
        required=False,
    )
    paste_content = schema.Float(
        title=_(
            u"title_mix_design_concrete_paste_content",
            default=u"Paste Content"),
        description=_(
            u"description_mix_design_concrete_paste_content",
            default=u"Unit used is Percentage (%)"),
        required=False,
    )
    super_air_meter = schema.Text(
        title=_(
            u"title_mix_design_concrete_super_air_meter",
            default=u"Super Air Meter #"),
        required=False,
    )


@implementer(IMixDesignConcrete, IMixDesignConcreteSchema, IDeactivable)
class MixDesignConcrete(Container):
    """Content-type class for IMixDesignConcrete"""

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
