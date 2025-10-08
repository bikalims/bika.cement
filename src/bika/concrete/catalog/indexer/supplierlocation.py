# -*- coding: utf-8 -*-

from plone.indexer import indexer
from bika.concrete.interfaces import ISupplierLocation


@indexer(ISupplierLocation)
def sortable_title(instance):
    """Uses the default Plone sortable_text index lower-case
    """
    title = instance.supplier_location_title
    return title.lower()
