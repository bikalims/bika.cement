# -*- coding: utf-8 -*-
#
# This file is part of SENAITE.CORE.
#
# SENAITE.CORE is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, version 2.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc., 51
# Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
# Copyright 2018-2021 by it's authors.
# Some rights reserved, see README and LICENSE.

import six
from archetypes.schemaextender.interfaces import IExtensionField
from bika.lims.browser.fields import UIDReferenceField
from plone.app.blob.field import FileField
from Products.Archetypes import public
from zope.interface import implements
from zope.site.hooks import getSite


class ExtensionField(object):
    """Mix-in class to make Archetypes fields not depend on generated
    accessors and mutators, and use AnnotationStorage by default.
    """

    implements(IExtensionField)
    storage = public.AnnotationStorage()

    def __init__(self, *args, **kwargs):
        super(ExtensionField, self).__init__(*args, **kwargs)
        self.args = args
        self.kwargs = kwargs

    def getAccessor(self, instance):
        def accessor():
            if self.getType().endswith("ReferenceField"):
                return self.get(instance.__of__(getSite()))
            else:
                return self.get(instance)

        return accessor

    def getEditAccessor(self, instance):
        def edit_accessor():
            if self.getType().endswith("ReferenceField"):
                return self.getRaw(instance.__of__(getSite()))
            else:
                return self.getRaw(instance)

        return edit_accessor

    def getMutator(self, instance):
        def mutator(value, **kw):
            if self.getType().endswith("ReferenceField"):
                self.set(instance.__of__(getSite()), value)
            else:
                self.set(instance, value)

        return mutator

    def getIndexAccessor(self, instance):
        name = getattr(self, "index_method", None)
        if name is None or name == "_at_accessor":
            return self.getAccessor(instance)
        elif name == "_at_edit_accessor":
            return self.getEditAccessor(instance)
        elif not isinstance(name, six.string_types):
            raise ValueError("Bad index accessor value: %r", name)
        else:
            return getattr(instance, name)


class ExtUIDReferenceField(ExtensionField, UIDReferenceField):
    "Field extender"


class ExtFileField(ExtensionField, FileField):
    "Field extender"
