# -*- coding: utf-8 -*-

from plone.dexterity.content import Container
from plone.supermodel import model
from zope.interface import implementer

from bika.concrete.interfaces import IBrands
from senaite.core.interfaces import IHideActionsMenu


class IBrandsSchema(model.Schema):
    """Schema interface
    """


@implementer(IBrands, IBrandsSchema, IHideActionsMenu)
class Brands(Container):
    """A folder/container for brands
    """
