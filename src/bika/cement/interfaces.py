# -*- coding: utf-8 -*-
"""Module where all interfaces, events and exceptions live."""


from zope.interface import Interface
from zope.publisher.interfaces.browser import IDefaultBrowserLayer


class IBikaCementLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""


class IMaterialTypeFolder(Interface):
    """Marker interface for material type setup folder
    """


class IMaterialClassFolder(Interface):
    """Marker interface for material class setup folder
    """


class ICuringMethodFolder(Interface):
    """Marker interface for curing meethod setup folder
    """


class IMixTypeFolder(Interface):
    """Marker interface for mix type setup folder
    """
