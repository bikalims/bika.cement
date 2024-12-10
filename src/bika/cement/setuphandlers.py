# -*- coding: utf-8 -*-
from Products.CMFPlone.interfaces import INonInstallable
from zope.interface import implementer
from bika.cement.config import PROFILE_ID
from bika.cement.config import logger
from bika.lims import api
from senaite.core.catalog import SETUP_CATALOG
from senaite.core.setuphandlers import (
    add_dexterity_items,
    setup_other_catalogs,
)


INDEXES = [
    (SETUP_CATALOG, "sort_key", "", "FieldIndex"),
]

COLUMNS = [
    (SETUP_CATALOG, "sort_key"),
]


@implementer(INonInstallable)
class HiddenProfiles(object):
    def getNonInstallableProfiles(self):
        """Hide uninstall profile from site-creation and quickinstaller."""
        return [
            "bika.cement:uninstall",
        ]


def post_install(context):
    """Post install script"""
    # Do something at the end of the installation of this package.
    logger.info("BIKA.CEMENT post install handler [BEGIN]")
    profile_id = PROFILE_ID
    context = context._getImportContext(profile_id)
    portal = context.getSite()
    add_dexterity_setup_items(portal)
    setup_catalogs(portal)
    add_mix_tab_to_batch(portal)


def uninstall(context):
    """Uninstall script"""
    # Do something at the end of the uninstallation of this package.


def add_dexterity_setup_items(portal):
    """Adds the Dexterity Container in the Setup Folder

    N.B.: We do this in code, because adding this as Generic Setup Profile in
          `profiles/default/structure` flushes the contents on every import.
    """
    # Tuples of ID, Title, FTI
    items = [
        ("materialtypes", "Material Types", "MaterialTypes"),
        ("materialclasses", "Material Classes", "MaterialClasses"),
        ("curingmethods", "Curing Methods", "CuringMethods"),
        ("mixtypes", "Mix Types", "MixTypes"),
        ("mixmaterials", "Mix Materials", "MixMaterials"),
    ]
    setup = api.get_senaite_setup()
    add_dexterity_items(setup, items)


def setup_catalogs(portal):
    """Setup catalogs"""
    setup_other_catalogs(portal, indexes=INDEXES, columns=COLUMNS)


def add_mix_tab_to_batch(portal):
    pt = api.get_tool("portal_types", context=portal)
    fti = pt.get("Batch")
    # Added location listing
    actions = fti.listActions()
    action_ids = [a.id for a in actions]
    if "mix" not in action_ids:
        fti.addAction(
            id="mix",
            name="Mix",
            permission="View",
            category="object",
            visible=True,
            icon_expr="string:${portal_url}/images/mix.png",
            action="string:${object_url}/mix",
            condition="",
            link_target="",
        )

    # add to allowed types
    allowed_types = fti.allowed_content_types
    if isinstance(allowed_types, tuple) or isinstance(allowed_types, list):
        allowed_types = list(allowed_types)
        if "MixDesign" not in allowed_types:
            allowed_types.append("MixDesign")
            fti.allowed_content_types = tuple(allowed_types)
            logger.info("Add MixDesign on Batches allowed types")
