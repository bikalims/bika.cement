# -*- coding: utf-8 -*-
from Products.CMFPlone.interfaces import INonInstallable
from zope.interface import implementer
from bika.cement.config import PROFILE_ID
from bika.cement.config import logger
from bika.lims import api
from senaite.core.setuphandlers import add_dexterity_items


@implementer(INonInstallable)
class HiddenProfiles(object):

    def getNonInstallableProfiles(self):
        """Hide uninstall profile from site-creation and quickinstaller."""
        return [
            'bika.cement:uninstall',
        ]


def post_install(context):
    """Post install script"""
    # Do something at the end of the installation of this package.
    logger.info("BIKA.CEMENT post install handler [BEGIN]")
    profile_id = PROFILE_ID
    context = context._getImportContext(profile_id)
    portal = context.getSite()
    add_dexterity_setup_items(portal)


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
        ("materialtype_folder",
         "Material Types",
         "MaterialTypeFolder"),
        ("materialclass_folder",
         "Material Classes",
         "MaterialClassFolder"),
        ("curingmethod_folder",
         "Curing Methods",
         "CuringMethodFolder"),
    ]
    setup = api.get_setup()
    add_dexterity_items(setup, items)
