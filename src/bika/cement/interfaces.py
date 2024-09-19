# -*- coding: utf-8 -*-
"""Module where all interfaces, events and exceptions live."""


from zope.interface import Interface
from zope.publisher.interfaces.browser import IDefaultBrowserLayer


class IBikaCementLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""


class IMaterialTypeFolder(Interface):
    """Marker interface for material types setup folder
    """


class IMaterialClassFolder(Interface):
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


class IMixMaterialFolder(Interface):
    """Marker interface for mix type setup folder
    """
