# -*- coding: utf-8 -*-
"""Module where all interfaces, events and exceptions live."""


from zope.interface import Interface
from zope.publisher.interfaces.browser import IDefaultBrowserLayer


class IBikaCementLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""


class IMaterialType(Interface):
    """Marker interface for material types
    """


class IMaterialTypes(Interface):
    """Marker interface for material types setup folder
    """


class IMaterialClass(Interface):
    """Marker interface for material classes
    """


class IMaterialClasses(Interface):
    """Marker interface for material classes setup folder
    """


class ICuringMethod(Interface):
    """Marker interface for curing methods
    """


class ICuringMethods(Interface):
    """Marker interface for curing methods setup folder
    """


class IMixType(Interface):
    """Marker interface for mix types
    """


class IMixTypes(Interface):
    """Marker interface for mix types setup folder
    """


class IMixMaterial(Interface):
    """Marker interface for mix materials
    """


class IMixMaterials(Interface):
    """Marker interface for mix materials setup folder
    """


class IMixDesign(Interface):
    """Marker interface for mix design
    """


class IMixDesignConcrete(Interface):
    """Marker interface for mix design
    """


class IMixDesignMortarPaste(Interface):
    """Marker interface for mix design
    """
