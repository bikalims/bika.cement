# -*- coding: utf-8 -*-
#
# This file is part of BIKA.CEMENT
#
# Copyright 2025 by it's authors.

import logging
from bika.lims.api import get_request
from bika.cement.interfaces import IBikaCementLayer
from zope.i18nmessageid import MessageFactory

PRODUCT_NAME = "bika.cement"
PROFILE_ID = "profile-{}:default".format(PRODUCT_NAME)
logger = logging.getLogger(PRODUCT_NAME)
_ = MessageFactory(PRODUCT_NAME)


def initialize(context):
    """Initializer called when used as a Zope 2 product."""

    logger.info("*** Initializing BIKA.CEMENT ***")


def is_installed():
    """Returns whether the product is installed or not"""
    request = get_request()
    return IBikaCementLayer.providedBy(request)
