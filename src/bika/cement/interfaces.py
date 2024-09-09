# -*- coding: utf-8 -*-
"""Module where all interfaces, events and exceptions live."""

from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from zope.interface import Interface

class IBikaCementLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""

class IMaterialClass(Interface):
    """Marker interface for material class
    """


class IMaterialClassFolder(Interface):
    """Marker interface for material class setup folder
    """