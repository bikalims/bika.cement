# -*- coding: utf-8 -*-

from plone.indexer import indexer

from bika.concrete.interfaces import IMixMaterialAmount
from bika.lims import api
from senaite.core.catalog.utils import sortable_sortkey_title


@indexer(IMixMaterialAmount)
def material_amount_class_sort_key(instance):
    m_amount = api.get_object_by_uid(instance.mix_material)
    m_types = m_amount.material_type
    if m_types:
        m_type = api.get_object_by_uid(m_types[0])
        m_classes = m_type.material_class
        if m_classes:
            m_class = api.get_object_by_uid(m_classes[0])
            return sortable_sortkey_title(m_class)

    sort_key = 999999
    return "{:010.3f}{}".format(sort_key, 'unsorted')
