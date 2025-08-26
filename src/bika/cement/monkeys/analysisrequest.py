# -*- coding: utf-8 -*-

from zope.component import getAdapters

from bika.cement.config import logger
from bika.lims import api
from bika.lims.interfaces import IAddSampleFieldsFlush


def get_mixmaterial_info(self, obj):
    """Returns the client info of an object
    """

    info = self.get_base_info(obj)
    if obj.supplier:
        supplier = api.get_object_by_uid(obj.supplier[0])
        info["field_values"].update(
            {"Supplier": self.to_field_value(supplier)}
        )

    return info


def get_supplier_queries(self, obj, record=None):
    """Returns the filter queries to apply to other fields based on both
    the SampleType object and record
    """
    path = api.get_path(obj)
    queries = {
        "SupplierContact": {
            "path": {
                "query": path,
            },
        },
        "SupplierLocation": {
            "path": {
                "query": path,
            },
        },
    }
    return queries


def ajax_get_flush_settings(self):
    """Returns the settings for fields flush

    NOTE: We automatically flush fields if the current value of a dependent
          reference field is *not* allowed by the set new query.
          -> see self.ajax_is_reference_value_allowed()
          Therefore, it makes only sense for non-reference fields!
    """
    flush_settings = {
        "Client": [
        ],
        "Contact": [
        ],
        "SampleType": [
        ],
        "PrimarySample": [
            "EnvironmentalConditions",
        ],
        "Supplier": [
            "SupplierContact",
            "SupplierLocation",
        ]
    }

    # Maybe other add-ons have additional fields that require flushing
    for name, ad in getAdapters((self.context,), IAddSampleFieldsFlush):
        logger.info("Additional flush settings from {}".format(name))
        additional_settings = ad.get_flush_settings()
        for key, values in additional_settings.items():
            new_values = flush_settings.get(key, []) + values
            flush_settings[key] = list(set(new_values))

    return flush_settings
