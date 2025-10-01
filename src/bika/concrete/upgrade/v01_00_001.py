# -*- coding: utf-8 -*-

import transaction

from bika.lims import api
from bika.concrete import PRODUCT_NAME
from bika.concrete import PROFILE_ID
from bika.concrete import logger
from bika.concrete.setuphandlers import setup_catalogs
from bika.concrete.setuphandlers import add_location_to_supplier
from bika.concrete.setuphandlers import setup_id_formatting

from senaite.core.catalog import SETUP_CATALOG, SENAITE_CATALOG
from senaite.core.upgrade import upgradestep

version = "1.0.2"
OLD_PACKAGE = 'bika.cement'
NEW_PACKAGE = 'bika.concrete'


@upgradestep(PRODUCT_NAME, version)
def upgrade(tool):
    portal = tool.aq_inner.aq_parent
    setup = portal.portal_setup
    ver_from = "1000"

    logger.info(
        "Upgrading {0}: {1} -> {2}".format(PRODUCT_NAME, ver_from, version)
    )

    # -------- ADD YOUR STUFF BELOW --------

    setup.runImportStepFromProfile(PROFILE_ID, "typeinfo")

    logger.info("{0} upgraded to version {1}".format(PRODUCT_NAME, version))
    return True


def reindex_mix_materials(tool):
    logger.info("Reindexing mix material ...")
    setup_catalogs(api.get_portal())
    cat = api.get_tool(SETUP_CATALOG)
    for brain in cat(portal_type="MixMaterial"):
        obj = brain.getObject()
        logger.info("Reindex mix material: %r" % obj)
        obj.reindexObject()
    for brain in cat(portal_type="MixMaterialAmount"):
        obj = brain.getObject()
        logger.info("Reindex mix material: %r" % obj)
        obj.reindexObject()
    logger.info("Reindexing mix materials [DONE]")


def add_brands(tool):
    portal = tool.aq_inner.aq_parent
    setup = portal.portal_setup
    # -------- ADD YOUR STUFF BELOW --------

    setup.runImportStepFromProfile(PROFILE_ID, "typeinfo")
    setup_id_formatting(portal)
    add_location_to_supplier(portal)


def migrate_cement_to_concrete(context):
    """Upgrade step to update ZODB objects from bika.cement to bika.concrete."""
    catalog = api.get_tool(SENAITE_CATALOG)

    migrated = 0
    skipped = 0
    failed = 0

    logger.info("Starting migration of objects from %s to %s",
                OLD_PACKAGE, NEW_PACKAGE)

    for brain in catalog():
        obj = None
        try:
            obj = brain.getObject()
            cls = obj.__class__
            module_name = cls.__module__
            class_name = cls.__name__

            if module_name.startswith(OLD_PACKAGE):
                # Attempt to import the new class
                new_module_name = module_name.replace(OLD_PACKAGE, NEW_PACKAGE, 1)
                try:
                    new_module = __import__(new_module_name, fromlist=[class_name])
                    new_class = getattr(new_module, class_name)
                except ImportError as e:
                    failed += 1
                    logger.warning("FAILED import for %s: %s (%s.%s)",
                                   brain.getPath(), e, module_name, class_name)
                    continue

                old_class_path = "{}.{}".format(module_name, class_name)
                new_class_path = "{}.{}".format(new_module_name, class_name)

                # Change the class of the object
                obj.__class__ = new_class
                migrated += 1
                logger.info("MIGRATED %s: %s → %s",
                            brain.getPath(), old_class_path, new_class_path)
            else:
                import pdb; pdb.set_trace()
                skipped += 1
                # Optionally log skipped objects, but keep it light
                # logger.debug("SKIPPED %s: %s.%s",
                #             brain.getPath(), module_name, class_name)
        except Exception as e:
            failed += 1
            path = getattr(brain, 'getPath', lambda: '(unknown)')()
            logger.warning("FAILED migration for %s: %s", path, e)

    transaction.commit()
    catalog.clearFindAndRebuild()

    logger.info("Migration summary: migrated=%s skipped=%s failed=%s",
                migrated, skipped, failed)
