# -*- coding: utf-8 -*-
#
# This file is part of BIKA CEMENT
#
# SENAITE.QUEUE is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the Free
# Software Foundation, version 2.
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
# Copyright 2019-2021 by it's authors.
# Some rights reserved, see README and LICENSE.

from bika.lims import api
from bika.cement import PRODUCT_NAME
from bika.cement import PROFILE_ID
from bika.cement import logger
from bika.cement.setuphandlers import setup_catalogs

from senaite.core.catalog import SETUP_CATALOG
from senaite.core.upgrade import upgradestep
from senaite.core.upgrade.utils import UpgradeUtils

version = "1.0.2"


@upgradestep(PRODUCT_NAME, version)
def upgrade(tool):
    portal = tool.aq_inner.aq_parent
    setup = portal.portal_setup
    ut = UpgradeUtils(portal)
    ver_from = "1000"

    if ut.isOlderVersion(PRODUCT_NAME, version):
        logger.info(
            "Skipping upgrade of {0}: {1} > {2}".format(PRODUCT_NAME, ver_from, version)
        )
        return True

    logger.info("Upgrading {0}: {1} -> {2}".format(PRODUCT_NAME, ver_from, version))

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
