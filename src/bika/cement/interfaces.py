# -*- coding: utf-8 -*-
"""Module where all interfaces, events and exceptions live."""


from zope.interface import Interface
from zope.publisher.interfaces.browser import IDefaultBrowserLayer


class IBikaCementLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""


class IMaterialTypeFolder(Interface):
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


class IMixTypeFolder(Interface):
    """Marker interface for mix types setup folder
    """


class IMixMaterial(Interface):
    """Marker interface for mix material
    """


class IMixMaterials(Interface):
    """Marker interface for mix material setup folder
    """
